# The Unofficial Guide — Project 1

**Demo:**[App Demo](https://github.com/Hluii/ai201-project1-unofficial-guide-starter/blob/main/DEMOred.mp4)

![App Demo](https://github.com/Hluii/ai201-project1-unofficial-guide-starter/blob/main/DEMOred.gif)

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

Chunk size was determined by Max character count on RateMyProfessor which is `350` and short reviews typically point to small chunks to keep precision high.
Overlap had near-zero effect because reviews are short and chunked individually. Only one review exceeded the 350 chunk size. All professors in 10 document dataset have 10+ reviews.
Preprocessing included normalizing course names, stripping quality/difficulty scores, all colon-metadata(Grades, Attendance, textbook, and etc.), tags, and reaction(helpful and thumbs up/down) footers.

**Final chunk count:**
1025 chunks

### Sample Chunks

<!-- 5 representative chunks produced by ingestion.py, each labeled with its
     source document. The "Professor: ... | Course: ..." header line is prepended
     to every chunk before embedding (see Spec Reflection). -->

**1. Source: `Anagha_Kulkarni_rmp.txt`** — Anagha Kulkarni · CSC 620 · Apr 26th, 2026
> Professor: Anagha Kulkarni | Course: CSC 620
> Took CS620 with this professor. I found the environment difficult for asking questions. When students sought clarification, she often responded with laughter rather than an explanation, which discouraged class participation. I'd recommend looking for a section that better fosters open discussion.

**2. Source: `Anthony_Souza_rmp.txt`** — Anthony Souza · CSC 101 · Dec 19th, 2025
> Professor: Anthony Souza | Course: CSC 101
> Prof Souza is amazing. I was terrified to take CSC and had a lot of preconceived notions about taking CSC, but all of those fears were shattered by how great a Prof he is. Every topic was presented in an understandable and digestible way. He treats every student with respect and truly wants to see you succeed. Def take his class.

**3. Source: `Daniel_Tomasevich_rmp.txt`** — Daniel Tomasevich · CSC 230 · Jan 27th, 2026
> Professor: Daniel Tomasevich | Course: CSC 230
> homework 15%, 2 midterms are 20% each, final is 45%. He reads off slides that he has forever and first day just jumps in material. Majority of the class was not passing, if you have trouble with taking test this might not be the best teacher to take. Teacher looks half sleep trying to teach the class behind his tablet. Not enthusiastic.

**4. Source: `Duc_Ta_rmp.txt`** — Duc Ta · CSC 340 · Jan 22nd, 2026
> Professor: Duc Ta | Course: CSC 340
> Work hard, and you will find this professor the best. He cares that you learn and be ready for the demands in the workplace. Always start assignments early and pay attention during lecture. You will enjoy his teaching thoroughly. He is a natural and genuine educator. His materials are enormously useful.

**5. Source: `Hui_Yang_rmp.txt`** — Hui Yang · CSC 340 · May 4th, 2026
> Professor: Hui Yang | Course: CSC 340
> The professor is unorganized in her lecture material; it is impossible to apply what is taught in class to your homework or tests. The textbook is $95 and will probably get more expensive. She posts no reviews or mock exams for you to practice for upcoming tests.

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

## Retrieval Test Results

<!-- 3 queries with the chunks retrieve() actually returned (all-MiniLM-L6-v2,
     cosine distance, k=5, cutoff=0.5). For at least 2, provide a written explanation of why the returned chunks are relevant to the query. -->

### Query 1 — "Is Anagha Kulkarni helpful?"
5 chunks returned within the 0.5 cutoff (closest first):

1. **dist 0.3814** · Anagha Kulkarni · CSC 675 · Aug 23rd, 2016
   > I felt like I learned a lot in her class. If you read the book, and do the work you will probably pass. She is very nice and will listen if you have a legitimate problem.
2. **dist 0.4267** · Anagha Kulkarni · CSC 620 · Jul 10th, 2021
   > Great professor. She knows what she is doing and is patient. If you don't show up and don't do the work you won't pass.
3. **dist 0.4317** · Anagha Kulkarni · CSC 620 · Oct 24th, 2024
   > She is very sweet and wants everyone to learn and succeed in the class, however, her lectures are not engaging; she reads from the slides and her explanations are vague. Quizes are kind of hard but if you learn the material you should do ok. Homework is outdated and sometimes difficult to understand so you do not really know what to do.

**Why these chunks are relevant:** These chunks were retrieved because "listening to problems," "patient," and "wanting everyone to succeed" all fall into the same semantic topic bucket as "helpful". "she will listen if you have a legitimate problem" lands close to a query asking about helpfulness even without the word "helpful" appearing. Notably these chunks skew positive about Kulkarni, while the negative reviews that drove the final answer were also in the top 5 but not shown here. Meaning that retrieval surfaced a balanced set for the LLM to reason 
over.

### Query 2 — "What is Daniel Tomasevich's class known for?"
5 chunks returned within the 0.5 cutoff; top 3 shown:

1. **dist 0.3168** · Daniel Tomasevich · CSC 212 · Dec 15th, 2006
   > Great teacher
2. **dist 0.3360** · Daniel Tomasevich · CSC 300 · May 31st, 2022
   > He is friendly. I enjoyed his lecture, and I have learned new interesting subjects. It has 4 quizzes which has 32 percentage of your grade. If you attend in his lecture, you will answer to his quizzes easily (there is no wrong or right answer). There are two essays has each one 4 pages plus one essay of 10 pages for final. He is generous in grading
3. **dist 0.3403** · Daniel Tomasevich · CSC 305 · Oct 15th, 2005
   > This was a VERY borring super-easy class. Just have to take a few (3-4) quizzes and do a paper. The professor does a weird eye-rolling thing that is really scary when you sit near the front. Be aware. You don't need to show up for class really. Most of the answers you can guess.

**Why these chunks are relevant:** All three of these chunks were retrieved, because they contained descriptions of class structure and teaching style. Chunk 1 is likely the closest match, because "great teacher" is a very strong phrase that aligns with the professor. Then chunk 2 and 3 both describe class and grading structure such as easy, how many quizzes, and attendance expectations.

### Query 3 — "Which SFSU CS professor is best for support and grade opportunities?"
5 chunks returned within the 0.5 cutoff; top 3 shown:

1. **dist 0.2471** · Duc Ta · CSC 220 · Jan 16th, 2026
   > He is the best computer science professor in SFSU. He gives you a lot of opportunities to boost your grade during the semester. His explanations are very clear.
2. **dist 0.3118** · Anthony Souza · CSC 413 · Jan 10th, 2020
   > He is one of the best CS teachers at SFSU. He is very nice and caring. I have learned a lot from his class. I wish I could take him more. Take him 100% you will not regret.
3. **dist 0.3167** · Duc Ta · CSC 340 · Nov 8th, 2021
   > Coming to SFSU only to take a couple of Computer Science courses, I found Professor Ta a huge surprise for me. He is better than all the professors I had at UC Davis. I did not expect such superior teaching quality and genuine care from an SFSU professor. Take him if you can. All his courses.

**Why these chunks are relevant:** Duc Ta and Anthony Souza both show up in this retrieval because the text is highly related to the query for "support" and "grade opportunities". Specifically mentioning Duc Ta giving grade boosts and opportunities in chunk 1 which maps extremely close to the query. Chunks 2 and 3 were pulled because "caring," "nice," and "genuine care" are semantically close to "support" in the embedding space. Overall all the passages also mentioned them by their role CS professor in SFSU which also gave these specific chunks a strong push to relevancy. The low distance scores across all three chunks (0.25–0.32) indicate this was the strongest retrieval of the three test queries.

> **Cutoff at work (off-domain):** the query *"What is the best taco truck in Oakland?"* returned **0 chunks** — the closest chunk sat at distance 0.6608, above the 0.5 cutoff, so nothing reached the LLM. (This is why the same query produces an "Insufficient data" refusal in the Example Responses below.)

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**

The system prompt explicitly instructs the model to answer using ONLY the 
provided context and never use outside or prior knowledge. The exact 
instruction given to the model is:

     "Use ONLY the provided context. Do NOT use any outside or prior knowledge. If the context does not contain enough information to answer, say so plainly instead of guessing. Ground every claim in what the reviewers actually wrote; do not invent details, professors, courses, or facts."

Temperature is set to `0.2` to reduce hallucination risk by making the model 
less creative and more conservative in its responses.

Structural grounding mechanisms:
Beyond the prompt, grounding is enforced structurally in two ways:

1. Distance cutoff: `retrieve()` filters out any chunk with a distance score 
above 0.5, so the LLM only receives chunks that are semantically close to 
the query. Loosely related chunks never reach the model.

2. Empty retrieval guard: if `retrieve()` returns no chunks within the cutoff, 
`generate_response()` returns "Insufficient data to answer this question." 
without ever calling the LLM. The model cannot hallucinate an answer 
because it is never invoked.

**How source attribution is surfaced in the response:**

Source attribution is handled programmatically, not left to the LLM. 
Each retrieved chunk is formatted with its metadata (professor name, course, 
date, filename) before being passed as context. After generation, 
`_format_sources()` builds a deduplicated list of professor names and source 
filenames drawn from chunk metadata and appended to every response. 
Attribution is guaranteed by the pipeline structure regardless of what 
the LLM produces.

### Example Responses

<!-- 2 in-domain responses (source attribution visible) + 1 out-of-scope refusal,
     captured from generate_response(). -->

**Example 1 — in-domain — "Which SFSU CS professor is best for support and grade opportunities?"**
> Based on the reviews, Professor Duc Ta is highlighted for providing "a lot of opportunities to boost your grade" and "a lot of extra credit opportunities" in his classes (CSC 220 and CSC 340), making him a strong candidate for support and grade opportunities. Additionally, reviewers praise his clear explanations and care for students, which suggests he is supportive. Professor Anthony Souza is also described as "very nice and caring," but the reviews do not specifically mention grade opportunities. Therefore, according to the provided context, Professor Duc Ta stands out for support and grade opportunities.
>
> **Sources:**
> - Duc Ta (Rate My Professors, file: Duc_Ta_rmp.txt)
> - Anthony Souza (Rate My Professors, file: Anthony_Souza_rmp.txt)

**Example 2 — in-domain — "What is Daniel Tomasevich's class known for?"**
> According to the reviews, Daniel Tomasevich's classes are known for being easy, with few quizzes and papers. One reviewer mentioned that his CSC 305 class was "VERY borring" and "super-easy", with only 3-4 quizzes and a paper, and that most answers can be guessed. Another reviewer mentioned that his CSC 300 class had 4 quizzes with no wrong or right answers, making it easy to answer if you attend the lectures. Additionally, he is described as a "great teacher" and "friendly", who is "generous in grading".
>
> **Sources:**
> - Daniel Tomasevich (Rate My Professors, file: Daniel_Tomasevich_rmp.txt)

**Example 3 — out-of-scope — "What is the best taco truck in Oakland?"**
> Insufficient data to answer this question.
>
> **Sources:** (none)

The out-of-scope query is refused without ever calling the LLM: retrieval returned 0 chunks within the 0.5 cutoff (see Retrieval Test Results), so `generate_response()` short-circuits to the fixed "Insufficient data" message.

---

## Query Interface

<!-- Describe the input/output fields and include one full query -> response transcript. -->

A Gradio web app (`app.py`), launched with `python app.py` and opened at http://localhost:7860. On first run it builds the ChromaDB index automatically.

**Input fields:**
- **Your question** — a single-line textbox for a natural-language question. An **Ask** button submits it; pressing Enter in the box also submits.
- **Filter by professor (optional)** — a dropdown of the 10 professors (plus "(any professor)") that restricts retrieval to one professor. *(stretch — see Metadata Filtering)*
- **Only reviews from year ≥** — a number input that drops reviews older than the given year (0 = no filter). *(stretch — see Metadata Filtering)*

**Output fields:**
- **Answer** — a 6-line textbox holding the grounded answer (or "Insufficient data to answer this question.").
- **Sources** — a 4-line textbox holding the deduplicated professor + filename list the answer drew from; shows "(no sources)" when nothing was retrieved.



**Sample interaction transcript:**

```
Question:  What is Daniel Tomasevich's class known for?

Answer:
According to the reviews, Daniel Tomasevich's classes are known for being easy,
with few quizzes and papers. One reviewer mentioned that his CSC 305 class was
"VERY borring" and "super-easy", with only 3-4 quizzes and a paper, and that
most answers can be guessed. Another reviewer mentioned that his CSC 300 class
had 4 quizzes with no wrong or right answers, making it easy to answer if you
attend the lectures. Additionally, he is described as a "great teacher" and
"friendly", who is "generous in grading".

Sources:
- Daniel Tomasevich (Rate My Professors, file: Daniel_Tomasevich_rmp.txt)
```

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
|1|Is Professor Anagha Kulkarni recommended for students who need a lot of in-class support?|No — unhelpful, vague, learn independently|"May not be recommended": unorganized, vague explanations, doesn't respond to emails, goes too fast|Relevant (all Kulkarni)|Accurate
|2|What happens if you miss too many classes in Robert Bierman's course?|	Auto-fail at 5+ absences	|Refused: "context does not contain enough info"|Off-target (recall miss)|Inaccurate (correct grounding, but failed to answer)
|3|What is Daniel Tomasevich's class known for?|Easy; boring/monotonous, argumentative quizzes|Easy, "super-easy," "VERY boring," quizzes with "no wrong/right answer"|Relevant|Accurate|
|4|Are John Roberts' assignments considered clear and fair?|No — harsh grading, unclear, time-consuming|"No": harsh grading, finds something wrong, unclear answers, time-consuming|Relevant|Accurate (right conclusion; missed the specific "unintentional mistakes / low pass rate")|
|5|Which SFSU CS professor is best for students who want a lot of support and grade opportunities?|Duc Ta — caring, grade-boosting, no mandatory attendance, free materials|Duc Ta: grade-boosting + extra-credit opportunities|Partially accurate (1 of 5 chunks was Anthony Souza)|Accurate|

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

**1. Question that failed:**

     What happens if you miss too many classes in Robert Bierman's course?

**What the system returned:**

     "The context does not contain enough information to answer what happens if you miss too many classes in Robert Bierman's course. The reviews provided discuss the difficulty of the course, grading, and the professor's teaching style, but do not mention the consequences of missing classes."

**Root cause (tied to a specific pipeline stage):**

     This is a retrieval recall failure at the embedding stage, not a generation bug. Notably, the generation layer handled it correctly by refusing to answer rather than hallucinating. The specific detail about Bierman's 5-absence auto-fail policy exists in the corpus (Bierman_rmp.txt) but was never retrieved. The attendance fact appears in a single sentence embedded inside a chunk whose overall meaning is dominated by general difficulty and grading language meaning that this dominant language is what the vector represents, not the attendance policy.

**What you would change to fix it:**

     A fix would be smaller chunks so that the attendance sentence gets its own embedding, or metadata tagging attendance-related facts explicitly.

**2. Question that failed:**

     Which professor is easiest?

**What the system returned:**

     Top 3 was John Roberts, 4th Daniel Tomasevich, 5th John Roberts. At a distance range of 0.3722 - 0.4075

**Root cause (tied to a specific pipeline stage):**

     Embedding stage, all-MiniLM-L6-v2 embeds the topic of course difficulty, but not the polarity as in how hard or easy. Also the words "easy" and "hard" are semantically on the same axis, therefore making them close.

**What you would change to fix it:**

     A fix would require either a reranking step after retrieval that scores for polarity, or a model trained on sentiment-aware embeddings.

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**

Notably the spec helped by informing my choice to diverge from ChromaDB's default L2 distance calculation to cosine, since I wanted a result that returned at a cut-off to weed out unrelated data before getting to generation.

**One way your implementation diverged from the spec, and why:**

One way my implementation diverged from the specification is that I chose to prepend the professor and course into the embedded text to skip filtering metadata at the generation stage. 

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

          It read through my rmp documents to create a predictable review structure from which it identified where data should be extracted. It created ingestion.py which includes: load, clean, and chunk document functions as well as a handful of helper functions. Then it returned a notice that retrieval may struggle if the text doesn't contain professor name, the choices were either to filter by metadata or prepend into embedded text.

- *What I changed or overrode:*

          I chose to prepend professor name and course info into the embedded text. Also, to normalize course name formatting and added a catch to turn non-3-digit course number into "Unknown" to handle bad source input from reviews.


**Instance 2**

- *What I gave the AI:*

          I gave Claude Code my retrieval section of planning.md and architecture diagram and told it to use the embedding model(all-MiniLM-L6-v2) and implement embed_and_store() to embed all chunks from chunk_document() to ChromaDB. Then used top-k to implement retrieve(query, top-k) using a cut-off of `.5` for distance to return top-k chunks of closest distance to the query under the cutoff. Then test retrievals accuracy based on my example questions.

- *What it produced:*

          Claude read through my given documents and verified the environment, and changed the default ChromaDB distance calculation from L2 to cosine in order to implement the 0.5 cutoff. Tested two off-domain and three on-domain queries and got expected results of 0 chunks for off-domain. Found a failure case in the "Which professor is easiest?" question, John Roberts was at the top and 4/5 chunks returned, yet the text reviews accompanying the chunks specifically denote him as the worst and difficult. 

- *What I changed or overrode:*

          I didn't change anything since fixing this would either: Require extra processing after retrieval to rank for polarity which would still have the same results just a different arrangement so I would need to retrieve more chunks to get the same "correct" chunk count or using a different embed model trained for sentiment-aware embeddings.

---

## Stretch Feature — Metadata Filtering

<!-- Stretch: filter retrieval by a metadata field, with a visible effect on results. -->

Every chunk stores `professor_name`, `course`, `date`, `year` (parsed from the date), `source`, and `filename`. `retrieve()` accepts optional `professor`, `course`, and `min_year` arguments and applies them through ChromaDB's `where` clause **before** the nearest-neighbour search, so a filter changes which chunks are eligible to return — not just a post-hoc trim. The Gradio UI exposes a **professor** dropdown and an **"only reviews from year ≥"** field.

### Demo A — date filter (`min_year=2020`)
Query: *"What is Daniel Tomasevich's class known for?"* — this targets Anticipated Challenge #2 (stale reviews skewing answers).

**Unfiltered** — top 5 include 2002/2005/2006 reviews, two of them empty "No Comments" entries:

| dist | Course | Date (year) | Review |
|---|---|---|---|
| 0.3168 | CSC 212 | Dec 15th, 2006 | Great teacher |
| 0.3360 | CSC 300 | May 31st, 2022 | He is friendly. I enjoyed his lecture… |
| 0.3403 | CSC 305 | Oct 15th, 2005 | This was a VERY borring super-easy class… |
| 0.3448 | CSC 212 | Mar 24th, 2005 | No Comments |
| 0.3448 | CSC 212 | Dec 15th, 2002 | No Comments |

**Filtered (`min_year=2020`)** — the pre-2020 chunks and the "No Comments" noise are gone; every result is 2021–2025:

| dist | Course | Date (year) | Review |
|---|---|---|---|
| 0.3360 | CSC 300 | May 31st, 2022 | He is friendly. I enjoyed his lecture… |
| 0.3768 | CSC 230 | Apr 28th, 2025 | I do not know how the university allows him to keep teaching… |
| 0.3815 | CSC 230 | Dec 30th, 2022 | …problems on the tests were much harder than homework… |
| 0.3828 | CSC 300 | Aug 8th, 2022 | 4 Online quizzes (no right/wrong answers)… |
| 0.3855 | CSC 300 | Mar 15th, 2021 | easy class. |

### Demo B — professor filter (`professor="Anthony Souza"`)
Query: *"Which professor gives lots of grade-boosting and extra-credit opportunities?"*

- **Unfiltered** — top results span multiple professors: John Roberts (0.3662), Robert Bierman (0.4221), Daniel Tomasevich (0.4296, 0.4326), Anthony Souza (0.4473).
- **Filtered to Anthony Souza** — only Souza chunks return (CSC 317 @ 0.4473, CSC 413 @ 0.4895); every other professor is excluded.

Metadata filtering by professor_name improves precision on named-professor queries but reduces recall on comparative queries like "which professor is easiest" where the system needs to reason across multiple professors simultaneously.
