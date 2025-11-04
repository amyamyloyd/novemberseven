I see the file now. Let me read it and tell you what it actually does.

Reading...

**What poc_agent.py actually does:**

1. **LangChain ChatOpenAI agent** with conversation memory
2. **Gathers requirements** using prompts from `poc_agent_prompts.json`
3. **Processes uploaded files**:
   - Wireframes (PNG/JPG) → analyzed via GPT-4 Vision
   - Documents (PDF/TXT/MD) → chunked and stored in FAISS vector store
4. **Semantic search** on uploaded docs for context
5. **Generates POC structure** when requirements complete:
   - Creates `poc_name` folder
   - Generates 3 phase markdown files (frontend, backend, database)
   - Creates README
   - Packages as ZIP download
6. **API endpoints**:
   - `/chat` - conversational interaction
   - `/upload` - file upload
   - `/generate` - trigger POC generation
   - `/download/{poc_name}` - download ZIP

**What it's missing:**

1. ❌ Doesn't read existing scaffold codebase (auth.py, database.py)
2. ❌ Still generates SQLite instructions, not MongoDB
3. ❌ Doesn't save PRD as standalone file Cursor can find
4. ❌ Doesn't generate test suites
5. ❌ Doesn't generate user/technical docs
6. ❌ Doesn't validate integration with existing code
7. ❌ No "is this a POC?" complexity analysis beyond prompts

What it does now: 
The **POC Agent** defined in `poc_agent.py` is a **Technical Product Manager AI** designed to help users build proof-of-concept (POC) applications from conversational input.

Here’s exactly what this agent does:

---

### 🧠 Core Purpose

* Acts as a **conversational AI product manager** that helps users design, document, and plan software POCs.
* Uses **LangChain** for conversation handling and **OpenAI’s GPT models** for reasoning, summarization, and content generation.

---

### 🗣️ Conversational Intelligence

* Gathers software requirements interactively through conversation.
* Remembers prior exchanges with **conversation memory** and maintains session continuity.
* Detects **contradictions or ambiguities** in user inputs and recommends simplifications.
* Determines next actions (e.g., “continue gathering,” “ready to generate,” etc.) based on the conversation stage.
* Provides stage-specific guidance and summaries for user confirmation.

---

### 📋 Requirements Extraction

* Extracts structured requirements using a **Pydantic schema** (`RequirementsSchema`) with fields:

  * `goal`, `users`, `workflow`, `frontend`, `backend`, `database`, `integrations`, `constraints`.
* Validates completeness and quality of the requirements.
* Updates requirements automatically from conversation transcripts.

---

### 🧩 RAG (Retrieval-Augmented Generation)

* Supports **document ingestion** (`pdf`, `txt`, `md`) using PyPDFLoader/TextLoader.
* Splits documents into chunks and creates **FAISS vector stores** per user for semantic retrieval.
* Uses **context retrieval** to answer questions with information from uploaded files.

---

### 🏗️ POC Generation

* Once requirements are approved, it auto-generates:

  * `poc_desc.md` – POC overview and goals.
  * `requirements.md` – Structured requirement summary.
  * `phase_1_frontend.md`, `phase_2_backend.md`, `phase_3_database.md` – Implementation plans for each layer.
* Uses prompt templates to fill in these markdown files with stack details (React, FastAPI, SQLite).

---

### 📘 PRD Generation

* Produces a full **Product Requirements Document (PRD)** with:

  * Overview, goals, user stories, stack specs, database models, API endpoints, and frontend requirements.
  * Implementation steps for Cursor AI to execute (including FastAPI, React, and testing/deployment checklists).

---

### 🖼️ Vision Capability

* Analyzes **wireframe images (PNG, JPG)** using **GPT-4 Vision**, extracting layout, components, styling, and UX notes.

---

### 💾 Persistence

* Can **save and reload conversations**, preserving the current stage, requirements, and chat history for long-term multi-session use.

---

### ✅ Summary of Key Actions

| Function                                      | Description                                                   |
| --------------------------------------------- | ------------------------------------------------------------- |
| `process_request()`                           | Handles user input, updates conversation, generates responses |
| `gather_requirements()`                       | Extracts structured POC data from chat                        |
| `detect_contradictions()`                     | Identifies conflicting or unclear requirements                |
| `suggest_simplification()`                    | Suggests simpler MVP-level features                           |
| `generate_poc()`                              | Creates markdown documents for the POC                        |
| `generate_prd()`                              | Generates full Product Requirements Document                  |
| `load_document()` / `create_vector_store()`   | Enables document-based RAG                                    |
| `analyze_wireframe()`                         | Uses GPT-4 Vision to interpret images                         |
| `save_conversation()` / `load_conversation()` | Maintains persistent session state                            |

---

In short, the **POC Agent** is a **multi-phase AI assistant** that goes from **chat-based requirement gathering → RAG-enhanced reasoning → document generation (PRD, POC files) → optional wireframe analysis**, effectively acting as an **AI product manager and architect** for proof-of-concept software builds.
