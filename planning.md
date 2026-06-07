# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->
Student Reviews of Computer Science professors from SFSU. Using Rate My Professors as a source. 

Valuable because this knowledge needs personal and up-to-date annecdotes, which is scattered and not conviently searchable.

---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 |Rate My Professors|Anagha Kulkarni|https://www.ratemyprofessors.com/professor/1840168|
| 2 |Rate My Professors|Daniel Tomasevich|https://www.ratemyprofessors.com/professor/727048|
| 3 |Rate My Professors|Kaz Okada|https://www.ratemyprofessors.com/professor/940009|
| 4 |Rate My Professors|Robert Bierman|https://www.ratemyprofessors.com/professor/2546440|
| 5 |Rate My Professors|Anthony Souza|https://www.ratemyprofessors.com/professor/1941294|
| 6 |Rate My Professors|Hui Yang|https://www.ratemyprofessors.com/professor/954738|
| 7 |Rate My Professors|Duc Ta|https://www.ratemyprofessors.com/professor/2316592|
| 8 |Rate My Professors|Jose Ortiz-Costa|https://www.ratemyprofessors.com/professor/2546744|
| 9 |Rate My Professors|John Roberts|https://www.ratemyprofessors.com/professor/1792558|
| 10 |Rate My Professors|Matt Pico|https://www.ratemyprofessors.com/professor/2069175|

---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:**
350 characters

**Overlap:**
50 characters

**Reasoning:**
Short reviews typical point to small chunks to keep precision high.Max charcter count on rate my professor is 350.

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:**
all-MiniLM-L6-v2

**Top-k:**
5

**Production tradeoff reflection:**
I am using a model taht can be run locally and is cheap right now. If I wasn't constrained by cost I would use paid options like OpenAI due to better accuracy. Also, since all the CS classes at SFSU are taught in english, multilingual support wouldn't be highly valued for me.

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | | |
| 2 | | |
| 3 | | |
| 4 | | |
| 5 | | |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1.

2.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

**Milestone 3 — Ingestion and chunking:**

**Milestone 4 — Embedding and retrieval:**

**Milestone 5 — Generation and interface:**
