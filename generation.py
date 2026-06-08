"""Grounded answer generation (pipeline stage 5).

Retrieves relevant review chunks, then asks Groq's llama-3.3-70b-versatile to
answer using ONLY that retrieved context. Source attribution (professor name +
filename) is built deterministically from the chunk metadata rather than left
to the model, so citations can never be hallucinated.
"""

import os

from dotenv import load_dotenv
from groq import Groq

from retrieval import retrieve

# Load GROQ_API_KEY (and anything else) from the project's .env.
load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"))

GROQ_MODEL = "llama-3.3-70b-versatile"
INSUFFICIENT_DATA = "Insufficient data to answer this question."

SYSTEM_PROMPT = (
    "You are The Unofficial Guide, answering questions about San Francisco State "
    "University Computer Science professors. You answer using ONLY the student "
    "reviews provided in the context below.\n\n"
    "Rules:\n"
    "- Use ONLY the provided context. Do NOT use any outside or prior knowledge.\n"
    "- If the context does not contain enough information to answer, say so "
    "plainly instead of guessing.\n"
    "- Ground every claim in what the reviewers actually wrote; do not invent "
    "details, professors, courses, or facts.\n"
    "- Be concise and specific, and refer to professors and courses by name when "
    "relevant.\n"
    "- The reviews are subjective student opinions, not official facts."
)

# Reuse one Groq client across calls.
_client = None


def _get_client():
    """Lazily create the Groq client from GROQ_API_KEY."""
    global _client
    if _client is None:
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            raise RuntimeError(
                "GROQ_API_KEY is not set. Copy .env.example to .env and add your "
                "key from https://console.groq.com"
            )
        _client = Groq(api_key=api_key)
    return _client


def _format_context(chunks):
    """Render retrieved chunks into a numbered, attributed context block."""
    blocks = []
    for i, chunk in enumerate(chunks, 1):
        meta = chunk["metadata"]
        # chunk["text"] starts with a "Professor: ... | Course: ..." header line;
        # drop it here since we lay out the metadata explicitly.
        review = chunk["text"].split("\n", 1)[-1]
        blocks.append(
            f"[{i}] Professor: {meta['professor_name']} | Course: {meta['course']} "
            f"| Date: {meta['date']} | Source: {meta['filename']}\n"
            f"Review: {review}"
        )
    return "\n\n".join(blocks)


def _format_sources(chunks):
    """Build a deduplicated source list (professor name + filename) from metadata."""
    seen = []
    for chunk in chunks:
        meta = chunk["metadata"]
        entry = (meta["professor_name"], meta["filename"], meta["source"])
        if entry not in seen:
            seen.append(entry)
    return "\n".join(
        f"- {prof} (Rate My Professors, file: {filename})"
        for prof, filename, _source in seen
    )


def generate_response(query, professor=None, course=None, min_year=None):
    """Answer ``query`` grounded only in retrieved Rate My Professors reviews.

    Args:
        query: The user's natural-language question.
        professor: Optional exact professor-name filter passed to retrieve().
        course: Optional exact course filter (e.g. "CSC 340").
        min_year: Optional minimum review year; keep reviews from then onward.

    Returns:
        A dict with:
            - ``answer``: the grounded answer string. If retrieval returns no
              chunks within the distance cutoff, this is
              "Insufficient data to answer this question."
            - ``sources``: a deduplicated, newline-separated list of professor
              names and source filenames the answer drew from ("" when none).
    """
    chunks = retrieve(query, professor=professor, course=course, min_year=min_year)
    if not chunks:
        return {"answer": INSUFFICIENT_DATA, "sources": ""}

    context = _format_context(chunks)
    user_message = (
        f"Context (student reviews from Rate My Professors):\n\n{context}\n\n"
        f"Question: {query}\n\n"
        "Answer using only the context above."
    )

    completion = _get_client().chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
        temperature=0.2,
    )
    answer = completion.choices[0].message.content.strip()

    return {"answer": answer, "sources": _format_sources(chunks)}


if __name__ == "__main__":
    for q in [
        "Is Anagha Kulkarni helpful?",
        "What happens if you miss too many classes in Robert Bierman's course?",
        "What is the best taco truck in Oakland?",  # off-domain -> insufficient data
    ]:
        result = generate_response(q)
        print(f"===== QUERY: {q!r} =====")
        print(f"ANSWER:\n{result['answer']}\n")
        print(f"SOURCES:\n{result['sources'] or '(none)'}\n")
