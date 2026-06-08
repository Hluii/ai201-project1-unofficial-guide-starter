# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

<!-- What topic or category of knowledge does your system cover?
     Why is this knowledge valuable, and why is it hard to find through official channels?
     Example: "Student reviews of CS professors at [university] — useful because official
     course descriptions don't reflect teaching style, exam difficulty, or workload." -->
Student Reviews of Computer Science professors from SFSU. Using Rate My Professors as a source. 

Valuable because this knowledge needs personal and up-to-date anecdotes, which are scattered and not conveniently searchable.
---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| # | Source | Type | URL or file path |
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

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:**
350 characters
**Overlap:**
50 characters
**Why these choices fit your documents:**
Chunk size was determined by Max character count on RateMyProfessor is 350 and short reviews typically point to small chunks to keep precision high.
Overlap had near-zero effect because reviews are short and chunked individually. Only one review exceeded the 350 chunk size. All professors in 10 document dataset have 10+ reviews.
Preprocessing included normalizing Course names, stripping quality/difficulty scores, All colon-metadata(Grades, Attendance, textbook, and etc...), tags, and reaction(helpful adn thumns up/down) footers.
**Final chunk count:**
1025 chunks
---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:**
all-MiniLM-L6-v2

**Production tradeoff reflection:**

I am using a model that can be run locally and is cheap right now. If I wasn't constrained by cost I would use paid options like OpenAI due to better accuracy. Also, since all the CS classes at SFSU are taught in English, multilingual support wouldn't be highly valued for me.
---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**

**How source attribution is surfaced in the response:**

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |
| 4 | | | | | |
| 5 | | | | | |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:**
Which professor is easiest?
**What the system returned:**
Top 3 was John Roberts, 4th Daniel Tomasevich, 5th John Roberts. At a distance range of 0.3722 - 0.4075
**Root cause (tied to a specific pipeline stage):**
Embedding stage, all-MiniLM-L6-v2 embeds topic of course difficulty, but not the polarity as in how hard or easy. Also the words "easy" and "hard" as semantically on the same axis, therefore making them close.
**What you would change to fix it:**
A fix would require either a reranking step after retrieval that scores for polarity, or a model trained on sentiment-aware embeddings.
---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**

**One way your implementation diverged from the spec, and why:**

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- *What I gave the AI:*

     I gave Claude my planning.md, architecture diagram, documents folder, and notes I have for how to clean the data(including structure to clean the raw txt and output to) and ask it to implement ingesting on text from /documents(load_document()) and clean each review into `Course, Review, Date`(clean_document). Then verify the input is cleaned; Then chunk according to my chunk size and overlap(chunk_document()). Returning chunks containing documents(raw text strings), metadata(Course, Professor Name, Source = `RateMyProfessor`, file name, and Date) and ids(unique chunk id).
- *What it produced:*
     It read through my rmp documents to create a predictable review structure from which it identified where data should be extracted. It created ingestion.py which includes: load, clean, and chunk document functions as well as a handful of helper functions. Then it returned a notice that retrieval may struggle if the text doesn't contain professor name, the choices were either to filter by metadata or preappend into embedded text.
- *What I changed or overrode:*
     I choose to preappend porofessor name and course info into the embedded text. Also, to normalize course name formatting and added a catch to turn non 3-digit course number into "Unknown" to handle bad source input from reviews.

**Instance 2**

- *What I gave the AI:*
I gave Claude Code my retrieval section of planning.md and architecture diagram and told it to use the embedding model(all-MiniLM-L6-v2) and implement embed_and_store() to embed all chunks from chunk_document() to ChromaDB. Then used top-k to implement retrieve(query, top-k) using a cut-off of `.5` for distance to return top-k chunks of closest distance to the query under the cutoff. Then test retrievals accuracy based on my example questions.

- *What it produced:*
Claude read throuhg my given documents and verified the environment, and changed the default chromaDB distance calculation from L2 to cosine in order to implement the 0.5 cutoff. Tested two off-domain and three on-domain queries and got expected results of 0 chunks for off-domain. Found a failure case in the "Which professor is easiest?" question, John Roberts was a the top and 4/5 chunks returned, yet the text reviews accompanying the chunks specifically denote him as the worst and difficult. 

- *What I changed or overrode:*
I didn't change anything since fixing this would either: Require extra processing after retrieval to rank for polarity which would still have the same results just a different arrangement so I would need to retrieve more chunks to get the same "correct" chunk count or using a different embed model trained for sentient-aware embeddings. 
