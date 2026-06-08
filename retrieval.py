"""Embedding, vector store, and retrieval (pipeline stages 3-4).

Takes the chunks produced by ``ingestion.chunk_document()``, embeds them with
all-MiniLM-L6-v2 (via sentence-transformers), and stores them in a local
persistent ChromaDB collection. ``retrieve()`` then embeds a query and returns
the top-k most similar chunks whose cosine distance is within a cutoff.

The collection uses cosine distance (``hnsw:space: cosine``), so distances fall
in [0, 2] where 0 == identical and a smaller number == more similar. This is
what makes the planning.md cutoff of 0.5 meaningful (keep cosine distance <=
0.5, i.e. cosine similarity >= 0.5). ChromaDB's default space is squared-L2,
for which 0.5 would be arbitrary.
"""

import os

import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

_BASE_DIR = os.path.dirname(os.path.abspath(__file__))

EMBED_MODEL_NAME = "all-MiniLM-L6-v2"
CHROMA_PATH = os.path.join(_BASE_DIR, "chroma_db")
COLLECTION_NAME = "professor_reviews"

# Loading the embedding model and opening the DB are expensive, so cache both at
# module scope and reuse across embed_and_store() / retrieve() calls.
_model = None
_client = None


def _get_model():
    """Lazily load and cache the sentence-transformers embedding model."""
    global _model
    if _model is None:
        _model = SentenceTransformer(EMBED_MODEL_NAME)
    return _model


def _get_client():
    """Lazily create and cache the persistent ChromaDB client."""
    global _client
    if _client is None:
        _client = chromadb.PersistentClient(
            path=CHROMA_PATH,
            settings=Settings(anonymized_telemetry=False),
        )
    return _client


def _embed(texts):
    """Embed a list of strings with the cached model, returned as plain lists."""
    model = _get_model()
    embeddings = model.encode(
        list(texts),
        normalize_embeddings=True,
        show_progress_bar=False,
    )
    return embeddings.tolist()


def embed_and_store(chunks):
    """Embed all chunks and (re)build the local ChromaDB collection.

    Each chunk's ``text`` is embedded with all-MiniLM-L6-v2 and stored alongside
    its full metadata (professor_name, course, date, source, filename) and id.
    The collection is rebuilt from scratch on every call so re-running never
    leaves stale or duplicate vectors behind.

    Args:
        chunks: Output of :func:`ingestion.chunk_document` -- dicts with
            ``text``, ``metadata`` (flat dict), and ``id``.

    Returns:
        The populated ChromaDB collection.
    """
    client = _get_client()

    # Drop any existing collection so the rebuild is clean and idempotent.
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass
    collection = client.create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )

    if not chunks:
        return collection

    ids = [c["id"] for c in chunks]
    documents = [c["text"] for c in chunks]
    metadatas = [c["metadata"] for c in chunks]
    embeddings = _embed(documents)

    # Add in batches to stay under ChromaDB's per-call limit on large corpora.
    batch_size = 1000
    for start in range(0, len(ids), batch_size):
        stop = start + batch_size
        collection.add(
            ids=ids[start:stop],
            embeddings=embeddings[start:stop],
            documents=documents[start:stop],
            metadatas=metadatas[start:stop],
        )

    return collection


def retrieve(query, k=5, cutoff=0.5):
    """Retrieve the top-k chunks most similar to ``query`` within a distance cutoff.

    Embeds the query with the same model, searches ChromaDB for the ``k`` nearest
    chunks, then drops any whose cosine distance exceeds ``cutoff``.

    Args:
        query: Natural-language query string.
        k: Number of nearest neighbors to fetch before filtering.
        cutoff: Maximum cosine distance to keep (smaller == more similar).

    Returns:
        A list of dicts (closest first), each with ``id``, ``text``,
        ``metadata``, and ``distance``. Empty if nothing is within the cutoff.
    """
    collection = _get_client().get_collection(COLLECTION_NAME)
    query_embedding = _embed([query])[0]

    result = collection.query(
        query_embeddings=[query_embedding],
        n_results=k,
        include=["documents", "metadatas", "distances"],
    )

    hits = []
    for id_, document, metadata, distance in zip(
        result["ids"][0],
        result["documents"][0],
        result["metadatas"][0],
        result["distances"][0],
    ):
        if distance <= cutoff:
            hits.append(
                {
                    "id": id_,
                    "text": document,
                    "metadata": metadata,
                    "distance": distance,
                }
            )
    return hits


if __name__ == "__main__":
    import ingestion

    documents_dir = os.path.join(_BASE_DIR, "documents")
    chunks = ingestion.ingest_corpus(documents_dir)

    print(f"Embedding {len(chunks)} chunks with {EMBED_MODEL_NAME} "
          f"(a few seconds on CPU)...")
    embed_and_store(chunks)
    print(f"Stored in ChromaDB at {CHROMA_PATH} (collection: {COLLECTION_NAME})\n")

    test_queries = [
        "Which professor is easiest?",
        "What do students say about Duc Ta?",
        "Is Anagha Kulkarni helpful?",
    ]

    K, CUTOFF = 5, 0.5
    for query in test_queries:
        print(f"===== QUERY: {query!r}  (k={K}, cutoff={CUTOFF}) =====")

        # Diagnostic: show the raw top-k with distances, marking which pass the
        # cutoff, so the cutoff choice can be evaluated.
        collection = _get_client().get_collection(COLLECTION_NAME)
        raw = collection.query(
            query_embeddings=[_embed([query])[0]],
            n_results=K,
            include=["documents", "metadatas", "distances"],
        )
        for rank, (doc, meta, dist) in enumerate(
            zip(raw["documents"][0], raw["metadatas"][0], raw["distances"][0]), 1
        ):
            mark = "KEEP    " if dist <= CUTOFF else "FILTERED"
            review = doc.split("\n", 1)[-1]  # strip the "Professor: ... | Course: ..." header
            print(f"  [{rank}] dist={dist:.4f} {mark} | "
                  f"{meta['professor_name']} | {meta['course']} | {meta['date']}")
            print(f"        {review}")

        kept = retrieve(query, k=K, cutoff=CUTOFF)
        print(f"  -> retrieve() returned {len(kept)} chunk(s) within cutoff {CUTOFF}\n")
