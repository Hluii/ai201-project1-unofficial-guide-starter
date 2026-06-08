# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->
Student Reviews of Computer Science professors from SFSU. Using Rate My Professors as a source. 

Valuable because this knowledge needs personal and up-to-date anecdotes, which are scattered and not conveniently searchable.

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
Short reviews typically point to small chunks to keep precision high. Max character count on RateMyProfessor is 350. All professors in 10 document dataset have 10+ reviews.

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
I am using a model that can be run locally and is cheap right now. If I wasn't constrained by cost I would use paid options like OpenAI due to better accuracy. Also, since all the CS classes at SFSU are taught in English, multilingual support wouldn't be highly valued for me.

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 |Is Professor Anagha Kulkarni recommended for students who need a lot of in-class support?|No — reviews say she is unhelpful with questions, has confusing slides, and students must learn independently.|
| 2 |What happens if you miss too many classes in Robert Bierman's course?|You automatically fail if you miss 5 or more classes.|
| 3 | What is Daniel Tomasevich's class known for?|Easy class with boring, monotonous lectures that read straight from a script. Quizzes are argumentative rather than right/wrong.|
| 4 |Are John Roberts' assignments considered clear and fair?|No — assignments frequently contain unintentional mistakes, are unclear, and a low percentage of students pass.|
| 5 |Which SFSU CS professor is best for students who want a lot of support and grade opportunities?|Duc Ta — reviewers consistently describe him as caring, patient, and offering many grade-boosting opportunities with no mandatory attendance and zero cost materials.|

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1. Inconsistent source information, because the source `RateMyProfessor` is a self-reported and biased dataset, the information may often conflict, leading to a confusing output `e.g. "___ is a great professor, they only lecture and are unreachable outside of class"`.

2. Noisy documents, responses may be "Inaccurate" if not taking into consideration date and Course. `e.g. "___ is terrible since they don't explain simple concepts well", when in reality these may be reviews for classes taught 10 years ago that are lower-division when the professor now teaches only upper division classes that get good reviews`.

---

## Architecture
![alt text](<Document Ingestion Flow to-2026-06-08-022244.png>)
     
     Document Ingestion(Clean) → Chunking(350 char chunk, 50 char Overlap) → Embedding(all-MiniLM-L6-v2) + Vector Store(ChromaDB) → Retrieval(top-k = 5) → Generation(Groq LLM)
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
     Ask Claude Code to help me set up file structure and leave functions like a fill-in-the-blank(To promote learning).

**Milestone 3 — Ingestion and chunking:**
I will give Claude Code my planning.md, architecture diagram, documents folder, and notes I have for how to clean the data(including structure to clean the raw txt and output to) and ask it to implement ingesting on text from /documents(load_document()) and clean each review into `Course, Review, Date`(clean_document). Then verify the input is cleaned; Then chunk according to my chunk size and overlap(chunk_document()). Returning chunks containing documents(raw text strings), metadata(Course, Professor Name, Source = `RateMyProfessor`, file name, and Date) and ids(unique chunk id). Then I will review a small sample size of chunks for quality and check the number of chunks against the size of input. Giving my feedback to Claude for improvement before moving on. 

**Milestone 4 — Embedding and retrieval:**
I will give Claude Code my retrieval section of planning.md and architecture diagram and tell it to use the embedding model(all-MiniLM-L6-v2) and implement embed_and_store() to embed all chunks from chunk_document() to ChromaDB. Then using top-k to implement retrieve(query, top-k) using a cut-off of `.5` for distance to return top-k chunks of closest distance to the query under the cutoff. Then test retrievals accuracy based on my example questions and have claude consult me on debugging.

**Milestone 5 — Generation and interface:**
 I will tell Claude to implement generate_response(query, retrieve_chunks(from retrieve())). The function will return "Insufficient data" when retrieve_chunks = [], only uses retrieve context(not trained knowledge), and attribute source(`RateMyProfessor`) and the `file name` from metadata. Then I will check for utilization of source material and implement UI with Gradio; Utilizing Claude Code for debugging.