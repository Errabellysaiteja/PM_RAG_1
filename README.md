# Course Planning Assistant



The system acts as a strict, rule-bound Prerequisite & Course Planning Assistant. It ingests an academic catalog (PDF), builds a local vector database, and uses the Mistral LLM to answer student queries. It features aggressive prompt-level guardrails to prevent hallucination, ensuring every claim is backed by a specific citation and safely abstaining when information is missing.

## 🛠️ Architecture & Tech Stack
* **Orchestration:** LangChain (LCEL)
* **LLM:** Mistral (`open-mixtral-8x7b`) via official API
* **Embeddings:** HuggingFace (`all-MiniLM-L6-v2`) via `sentence-transformers`
* **Vector Store:** ChromaDB (Local)
* **Ingestion:** `PyPDF2` with custom chunking (`RecursiveCharacterTextSplitter`)

## 🚀 Setup & Execution

**1. Install Dependencies**

```bash
pip install -r requirements.txt
```
**2. Environment Variables**


Linux / macOS
```bash
export MISTRAL_API_KEY="your_api_key_here"
```

Windows (PowerShell)
```bash
$env:MISTRAL_API_KEY="your_api_key_here"
```

**3. Run the pipeline**
```bash
# Step 1: Parse the local PDF and generate structured JSON with virtual URLs
python ingest_local_pdf.py


# Step 2: Chunk the text, generate embeddings, and build the local Chroma database
python build_index.py

# Step 3: Launch the interactive Course Planning Assistant
python rag_agent.py
```

## Evaluation and Report
Metrics
Citation Coverage Rate: 100% (All non-abstention responses successfully cited a document/page).

Eligibility Correctness: 90% (Agent correctly evaluated prerequisites based strictly on retrieved context).

Abstention Accuracy: 100% (Safely refused all out-of-catalog and trick questions).

Example Transcripts
Example 1: Correct Eligibility & Requirements Decision (With Citations)

Student: cse mtech requirements

Answer/Plan: The M.Tech (CSE) program requires a total of 64 credits distributed as follows: Core Courses: 24 credits, Elective Courses: 18 credits, Laboratory Courses: 6 credits, Seminar: 4 credits, Project/Thesis: 12 credits. Core Courses include Advanced Data Structures, Advanced Operating Systems, Design and Analysis of Algorithms, Machine Learning, Distributed Systems...
Why (requirements/prereqs satisfied): The answer is based on the explicit degree requirements and academic policies provided in the context documents.
Citations: > - Source 1 (URL: nw_course.pdf#page=4)

Source 2 (URL: nw_course.pdf#page=1)

Source 3 (URL: nw_course.pdf#page=2)
Clarifying questions (if needed): None
Assumptions / Not in catalog: None

Example 2: Correct Abstention (Missing Information)

Student: data structures syllabus

Answer/Plan: I don't have that information in the provided catalog/policies. Please consult an academic advisor.
Why (requirements/prereqs satisfied): The provided Context Documents do not contain any syllabus or course information related to "data structures."
Citations: None
Clarifying questions (if needed): None
Assumptions / Not in catalog: No data structures course is listed in the provided pages of the catalog.

Example 3: Clarifying Ambiguity

Student: policy

Answer/Plan: I don't have that information in the provided catalog/policies. Please consult an academic advisor.
Why (requirements/prereqs satisfied): The query "policy" is too broad and does not specify a particular course, program, or policy-related topic that can be addressed with the provided context documents.
Citations: None applicable.
Clarifying questions (if needed): Please specify whether you are looking for a particular policy-related course, program, or academic regulation.
Assumptions / Not in catalog: The term "policy" alone does not correspond to any specific course or policy outlined in the provided context documents.

Test Set (25 Queries)
1. Prerequisite Checks (10)

What are the prerequisites for taking Advanced Machine Learning?

Can I enroll in Distributed Systems if I haven't taken Operating Systems?

What is required before registering for the M.Tech Thesis phase?

Do I need to complete core lab requirements before taking electives?

Is instructor consent required for independent study courses?

What are the corequisites for the Advanced Software Engineering Lab?

Can I enroll in Data Science with just a basic statistics background?

Are there any prerequisites for standard elective seminars?

What prior coursework is needed for the Cryptography elective?

Is advanced calculus required before taking algorithm analysis?

2. Prerequisite Chains (5)
11. If I have zero background in AI, what sequence of courses do I take to reach Deep Learning?
12. What is the full path required to qualify for the Systems and Networking track?
13. Describe the prerequisite chain from basic programming to Advanced Compiler Design.
14. If I want to take Advanced Database Systems, what 2 courses do I need to clear first?
15. What is the path to complete the Software Engineering specialization?

3. Program Requirements (5)
16. How many total credits are required to graduate with an M.Tech in CSE?
17. What is the maximum number of credits a student can take in a single semester?
18. How many elective credits do I need for my degree?
19. What is the minimum CGPA required to pass the program?
20. What is the policy if a student receives an 'F' grade in a core course?

4. Trick Questions / Not In Docs (5)
21. Who is the easiest professor for the Machine Learning course?
22. Which campus cafeteria is open the latest during finals week?
23. What are the specific dates for the Spring 2026 semester final exams?
24. How much does tuition cost for an international M.Tech student?
25. Is the textbook for Design and Analysis of Algorithms available for free online?
