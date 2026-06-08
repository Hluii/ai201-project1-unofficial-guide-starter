"""Minimal Gradio UI for The Unofficial Guide.

One question box in, an answer box and a sources box out, wired to
generation.generate_response().

Run: python app.py  (then open the printed local URL)
"""

import os

import gradio as gr

import ingestion
import retrieval
from generation import generate_response

_BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Sentinel for the "no professor filter" option in the dropdown.
ANY_PROFESSOR = "(any professor)"


def _ensure_index():
    """Build the ChromaDB index on first run if it isn't already populated.

    retrieve() needs the collection to exist; this makes the app self-contained
    so it works even on a fresh checkout where embed_and_store() hasn't run yet.
    """
    try:
        collection = retrieval._get_client().get_collection(retrieval.COLLECTION_NAME)
        if collection.count() > 0:
            return
    except Exception:
        pass
    chunks = ingestion.ingest_corpus(os.path.join(_BASE_DIR, "documents"))
    retrieval.embed_and_store(chunks)


def _professor_choices():
    """Professor display names from the documents folder, for the filter dropdown."""
    docs = os.path.join(_BASE_DIR, "documents")
    names = sorted(
        ingestion._professor_name_from_filename(n)
        for n in os.listdir(docs)
        if n.lower().endswith(".txt")
    )
    return [ANY_PROFESSOR] + names


def answer_question(query, professor, min_year):
    """Gradio handler: return (answer, sources), honoring optional metadata filters."""
    if not query or not query.strip():
        return "Please enter a question.", ""
    prof = None if not professor or professor == ANY_PROFESSOR else professor
    year = int(min_year) if min_year else None
    result = generate_response(query, professor=prof, min_year=year)
    return result["answer"], result["sources"] or "(no sources)"


with gr.Blocks(title="The Unofficial Guide — SFSU CS Professors") as demo:
    gr.Markdown(
        "# The Unofficial Guide for SFSU CS Professors\n"
        "Ask about **SFSU Computer Science professors**. Answers come *only* from "
        "student reviews on Rate My Professors — not the model's general knowledge."
    )
    question = gr.Textbox(
        label="Your question",
        placeholder="e.g. Is Anagha Kulkarni helpful? What is Duc Ta like?",
    )
    with gr.Row():
        professor = gr.Dropdown(
            choices=_professor_choices(),
            value=ANY_PROFESSOR,
            label="Filter by professor (optional)",
        )
        min_year = gr.Number(
            value=0,
            precision=0,
            label="Only reviews from year ≥  (0 = no filter)",
        )
    ask = gr.Button("Ask", variant="primary")
    answer = gr.Textbox(label="Answer", lines=6)
    sources = gr.Textbox(label="Sources", lines=4)

    _inputs = [question, professor, min_year]
    ask.click(answer_question, inputs=_inputs, outputs=[answer, sources])
    question.submit(answer_question, inputs=_inputs, outputs=[answer, sources])


if __name__ == "__main__":
    _ensure_index()
    demo.launch()
