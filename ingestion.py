"""Document ingestion and chunking for The Unofficial Guide (Project 1).

Pipeline stage 1: Document Ingestion (Clean) -> Chunking.

Source documents live in ``documents/`` -- one ``.txt`` file per SFSU CS
professor, copy-pasted from Rate My Professors. Each file is a sequence of
review blocks with this repeating structure::

    Quality
    5.0
    Difficulty
    3.0
    [Computer Icon]CSC520        <- course (sometimes "Computer Icon" prefix)
    May 30th, 2026               <- date
    For Credit: Yes              <- 0+ metadata lines (colon-prefixed)
    Attendance: Not Mandatory
    Would Take Again: Yes
    Grade: A
    Textbook: Yes
    Online Class: Yes
    <the actual free-text review comment>
    Tough grader                 <- 0-3 canned RMP "tags"
    EXTRA CREDIT
    Helpful                      <- UI artifact / footer
    Thumbs up
    0
    Thumbs down
    0

This module keeps only the free-text comment (plus Course and Date) and drops
everything else (scores, metadata fields, canned tags, the "Helpful"/thumbs
footer), then chunks each review for embedding.
"""

import os
import random
import re

# Constant source label stamped onto every chunk's metadata.
SOURCE = "RateMyProfessors"

# Canned, finite-vocabulary RMP "tags" that appear on their own lines between
# the review comment and the "Helpful" footer. These are UI labels, not the
# student's written comment, so they are stripped. Stored normalized
# (lowercased) for case-insensitive matching ("EXTRA CREDIT" == "Extra credit").
RMP_TAGS = {
    "amazing lectures",
    "caring",
    "respected",
    "inspirational",
    "tough grader",
    "gives good feedback",
    "lots of homework",
    "extra credit",
    "accessible outside class",
    "clear grading criteria",
    "participation matters",
    "group projects",
    "lecture heavy",
    "get ready to read",
    "graded by few things",
    "test heavy",
    "tests are tough",
    "hilarious",
    "skip class? you won't pass.",
    "beware of pop quizzes",
    "online savvy",
    "so many papers",
}

# A review block's non-comment metadata lines, e.g. "Grade: A", "Textbook: N/A".
# Used to skip the metadata region that sits between the date and the comment.
# "Reviewed:" is included as defensive hardening: copy-paste from RMP can shift a
# "Reviewed: <date>" line off the review it belongs to. In this corpus it always
# lands between blocks (so the outer loop skips it anyway), but matching it here
# guarantees it can never leak into review text even if a future paste misplaces it.
_META_PREFIX_RE = re.compile(
    r"^(For Credit|Attendance|Would Take Again|Grade|Textbook|Online Class|Reviewed)\s*:",
    re.IGNORECASE,
)

# A standalone Quality/Difficulty score line, e.g. "5.0" or "1.5".
_SCORE_RE = re.compile(r"^\d+(?:\.\d+)?$")

# Leading "Computer Icon" artifact glued onto some course codes.
_ICON_PREFIX_RE = re.compile(r"^computer icon", re.IGNORECASE)

# Canonical SFSU CS course code = "CSC" + exactly 3 digits. The source data is
# noisy: case variants (Csc230), missing 'C' (CS340), bare numbers (340),
# stray leading zeros (CSC0413), and embedded spaces (CSC 872). This pattern
# (applied after upper-casing and removing spaces) recovers the 3-digit number
# from all of those. Codes that don't reduce cleanly (e.g. "CSC510645675",
# "CSC675CSC510", "13327") are treated as UNKNOWN_COURSE.
_COURSE_CODE_RE = re.compile(r"(?:CSC|CS)?0*(\d{3})")
UNKNOWN_COURSE = "Unknown"


def _professor_name_from_filename(filename):
    """Derive a display name from a file name: 'Matt_Pico_rmp.txt' -> 'Matt Pico'."""
    stem = os.path.splitext(os.path.basename(filename))[0]
    stem = re.sub(r"_rmp$", "", stem, flags=re.IGNORECASE)
    return stem.replace("_", " ").strip()


def _normalize_course(course):
    """Normalize a raw course line to canonical 'CSC NNN' form.

    Strips the 'Computer Icon' prefix, upper-cases, removes spaces, and reduces
    case/prefix/leading-zero variants to 'CSC ' + the 3-digit course number.
    Returns ``UNKNOWN_COURSE`` for codes that don't cleanly reduce.
    """
    raw = _ICON_PREFIX_RE.sub("", course).upper().replace(" ", "").strip()
    match = _COURSE_CODE_RE.fullmatch(raw)
    if match:
        return f"CSC {match.group(1)}"
    return UNKNOWN_COURSE


def _strip_trailing_tags(body_lines):
    """Drop canned RMP tag lines from the end of a review body.

    Tags always trail the comment, so we pop matching lines off the end until we
    hit real comment text. Returns the comment joined into a single string.
    """
    end = len(body_lines)
    while end > 0 and body_lines[end - 1].strip().lower() in RMP_TAGS:
        end -= 1
    return " ".join(line.strip() for line in body_lines[:end]).strip()


def load_document(filepath):
    """Load the raw text of a single document.

    Args:
        filepath: Path to a ``.txt`` source file.

    Returns:
        The file's full contents as a string.
    """
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


def clean_document(text, professor_name):
    """Strip all non-review content and return one structured record per review.

    Removes Quality/Difficulty scores, colon-prefixed metadata fields
    (For Credit, Attendance, Would Take Again, Grade, Textbook, Online Class),
    canned RMP tags, and the "Helpful"/thumbs-up/thumbs-down footer. Keeps only
    the student's free-text comment plus its Course and Date.

    Args:
        text: Raw document text (e.g. from :func:`load_document`).
        professor_name: Display name of the professor this document is about.

    Returns:
        A list of dicts, each with keys: ``professor_name``, ``course``,
        ``review`` (the cleaned comment), and ``date``. Reviews with no
        free-text comment (tags only) are skipped.
    """
    lines = text.splitlines()
    n = len(lines)
    records = []
    i = 0

    while i < n:
        stripped = lines[i].strip()

        # A review block starts with "Quality" followed by a numeric score.
        is_block_start = (
            stripped.lower() == "quality"
            and i + 1 < n
            and _SCORE_RE.match(lines[i + 1].strip())
        )
        if not is_block_start:
            i += 1
            continue

        # Skip "Quality" + score, then "Difficulty" + score.
        i += 2
        if i < n and lines[i].strip().lower() == "difficulty":
            i += 1
            if i < n and _SCORE_RE.match(lines[i].strip()):
                i += 1

        # Course is the next non-empty line; date is the one after it.
        while i < n and not lines[i].strip():
            i += 1
        course = _normalize_course(lines[i].strip()) if i < n else ""
        i += 1

        while i < n and not lines[i].strip():
            i += 1
        date = lines[i].strip() if i < n else ""
        i += 1

        # Skip the colon-prefixed metadata region.
        while i < n and _META_PREFIX_RE.match(lines[i].strip()):
            i += 1

        # Collect the review body (comment + trailing tags) until the "Helpful"
        # footer, the next block (footer can be missing), or end of file.
        body = []
        while i < n:
            line = lines[i].strip()
            if line.lower() == "helpful":
                break
            if (
                line.lower() == "quality"
                and i + 1 < n
                and _SCORE_RE.match(lines[i + 1].strip())
            ):
                break
            if line:
                body.append(line)
            i += 1
        # The "Helpful"/thumbs footer is left for the outer loop to skip over.

        review = _strip_trailing_tags(body)
        if review:
            records.append(
                {
                    "professor_name": professor_name,
                    "course": course,
                    "review": review,
                    "date": date,
                }
            )

    return records


def _split_review(review, chunk_size, overlap):
    """Sliding-window split of a single review string into <= chunk_size pieces."""
    review = review.strip()
    if not review:
        return []
    if len(review) <= chunk_size:
        return [review]

    step = max(1, chunk_size - overlap)
    chunks = []
    start = 0
    while start < len(review):
        piece = review[start : start + chunk_size].strip()
        if piece:
            chunks.append(piece)
        if start + chunk_size >= len(review):
            break
        start += step
    return chunks


def chunk_document(records, chunk_size=350, overlap=50):
    """Chunk cleaned review records into embedding-ready chunk dicts.

    Each review is chunked independently (so a chunk never mixes two reviews),
    using a sliding window of ``chunk_size`` characters with ``overlap``
    characters of carry-over. Most RMP reviews are <= 350 chars and yield a
    single chunk.

    Args:
        records: Cleaned records from :func:`clean_document`. Each should carry
            ``professor_name``, ``course``, ``review``, ``date``, and (for
            attribution) ``filename``.
        chunk_size: Maximum characters per chunk.
        overlap: Characters of overlap between consecutive chunks of one review.

    The professor name and course are prepended to each chunk's ``text`` so the
    embedding captures who/what the review is about (reviews rarely name the
    professor themselves). Format::

        Professor: <name> | Course: <course>
        <review chunk>

    Note: the 350-char window is applied to the review text only; the prepended
    header adds ~40 chars on top, still well within the embedding model's limit.

    Returns:
        A list of dicts, each with:
            - ``text``: the chunk string (header + review chunk)
            - ``metadata``: {professor_name, course, date, source, filename}
            - ``id``: a unique string id for the chunk
    """
    chunks = []
    for record_idx, record in enumerate(records):
        filename = record.get("filename", "")
        stem = os.path.splitext(filename)[0] if filename else "doc"
        header = f"Professor: {record['professor_name']} | Course: {record['course']}"

        pieces = _split_review(record["review"], chunk_size, overlap)
        for chunk_idx, piece in enumerate(pieces):
            chunks.append(
                {
                    "text": f"{header}\n{piece}",
                    "metadata": {
                        "professor_name": record["professor_name"],
                        "course": record["course"],
                        "date": record["date"],
                        "source": SOURCE,
                        "filename": filename,
                    },
                    "id": f"{stem}-r{record_idx}-c{chunk_idx}",
                }
            )
    return chunks


def ingest_file(filepath, chunk_size=350, overlap=50):
    """Run load -> clean -> chunk for one file, wiring in professor_name + filename.

    This thin orchestrator exists because the assignment's ``chunk_document``
    signature does not receive the file path; it derives ``professor_name`` and
    ``filename`` here and stamps ``filename`` onto each record so the chunk
    metadata can carry source attribution.
    """
    professor_name = _professor_name_from_filename(filepath)
    filename = os.path.basename(filepath)

    text = load_document(filepath)
    records = clean_document(text, professor_name)
    for record in records:
        record["filename"] = filename

    return chunk_document(records, chunk_size=chunk_size, overlap=overlap)


def ingest_corpus(documents_dir, chunk_size=350, overlap=50):
    """Ingest every ``.txt`` file in ``documents_dir`` into one list of chunks."""
    all_chunks = []
    for name in sorted(os.listdir(documents_dir)):
        if not name.lower().endswith(".txt"):
            continue
        all_chunks.extend(
            ingest_file(
                os.path.join(documents_dir, name),
                chunk_size=chunk_size,
                overlap=overlap,
            )
        )
    return all_chunks


if __name__ == "__main__":
    documents_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "documents")
    chunks = ingest_corpus(documents_dir)

    print(f"Ingested {len(chunks)} chunks from {documents_dir}\n")

    sample = random.sample(chunks, min(5, len(chunks)))
    for n, chunk in enumerate(sample, 1):
        meta = chunk["metadata"]
        print(f"--- Sample chunk {n}/{len(sample)} ---")
        print(f"id:       {chunk['id']}")
        print(f"prof:     {meta['professor_name']}")
        print(f"course:   {meta['course']}")
        print(f"date:     {meta['date']}")
        print(f"source:   {meta['source']}")
        print(f"filename: {meta['filename']}")
        print(f"text ({len(chunk['text'])} chars): {chunk['text']}")
        print()
