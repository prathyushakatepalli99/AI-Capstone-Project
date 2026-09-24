# Zepto Support Assistant

## 1. Project Overview

This project implements a Zepto customer support assistant using a Retrieval-Augmented Generation (RAG) architecture.

The application uses Zepto policy documents as its knowledge base. User questions are classified as either policy-related or general questions.

For policy-related questions, the system retrieves relevant documents from ChromaDB and generates an answer using the retrieved context.

For general questions, the system returns a predefined response without performing retrieval.

The application runs in mock mode by default, so no external LLM API key is required.

### Overall Flow

Policy Documents → Embeddings → ChromaDB → User Query → Intent Classification → Retrieval → Answer → FastAPI Response

---

## 2. Technologies Used

- Python 3.11
- Sentence Transformers
- `all-MiniLM-L6-v2`
- ChromaDB
- LangGraph
- Pydantic
- FastAPI
- Uvicorn
- Dockerfile

---

## 3. Project Structure

```text
support_assistant/
│
├── docs/
│   ├── doc_01.txt
│   ├── doc_02.txt
│   ├── doc_03.txt
│   ├── doc_04.txt
│   ├── doc_05.txt
│   ├── doc_06.txt
│   ├── doc_07.txt
│   └── doc_08.txt
│
├── chroma_db/
│
├── ingest.py
├── prompt.py
├── graph.py
├── main.py
├── requirements.txt
├── Dockerfile
└── README.md

4. Knowledge Base

The knowledge base contains 8 Zepto policy documents.

Document	Policy
doc_01.txt	Delivery Policy
doc_02.txt	Returns & Refunds
doc_03.txt	Membership Tiers
doc_04.txt	Order Tracking
doc_05.txt	Order Cancellation
doc_06.txt	Damaged or Missing Items
doc_07.txt	Gift Cards
doc_08.txt	Customer Support Hours

5. Data Ingestion

The ingest.py script performs the following steps:

Reads all .txt files from the docs directory.
Loads the all-MiniLM-L6-v2 embedding model.
Generates embeddings for the policy documents.
Creates a persistent ChromaDB client.
Stores the documents and embeddings in ChromaDB.
Uses cosine similarity for retrieval.

The ChromaDB database is stored in:

chroma_db/

The collection name is:

zepto_policies

Cosine similarity is configured using:

metadata={"hnsw:space": "cosine"}
Run ingestion
python ingest.py

The script verifies the number of documents stored and prints their IDs.

Expected document IDs:

doc_01
doc_02
doc_03
doc_04
doc_05
doc_06
doc_07
doc_08
6. Embedding Model

The project uses the Sentence Transformers model:

all-MiniLM-L6-v2

The model converts both policy documents and user queries into numerical vector embeddings.

The embeddings are stored in ChromaDB and used for semantic similarity search.

7. Prompt Template

The prompt template is implemented in prompt.py.

The prompt contains the following sections:

Role
Context
Task
Format
Few-shot example
Length
User question

The prompt also contains explicit instructions not to use information outside the retrieved context.

Example constraint:

Do not answer using information that is not present in the provided context.
Do not make up or assume Zepto policies.

A few-shot example is included to demonstrate the expected response format.

8. LangGraph Workflow

The LangGraph workflow is implemented in graph.py.

The graph contains three main nodes:

                  classify_intent
                  /              \
                 /                \
             policy              general
               |                    |
               v                    v
    retrieve_and_answer       direct_answer
               |                    |
               v                    v
              END                  END
Node 1: classify_intent

This node classifies the user's question as either:

policy

or:

general

The following keywords are used for policy classification:

delivery
return
refund
membership
tracking
cancel
gift card
support hours

If the query contains one of these keywords, it is classified as a policy question.

Otherwise, it is classified as a general question.

Node 2: retrieve_and_answer

This node handles policy questions.

The process is:

Convert the user query into an embedding.
Search ChromaDB using cosine similarity.
Retrieve the top 3 relevant documents.
Use the top retrieved document to construct the mock answer.
Return the retrieved document IDs as sources.
Validate the final output using Pydantic.

Example mock response format:

Based on the retrieved context: <retrieved policy text>
Node 3: direct_answer

This node handles general questions.

No ChromaDB retrieval is performed.

In mock mode, the system returns:

I can only answer questions about Zepto policies right now.

The sources list is empty for general questions.

9. Mock LLM Mode

The application runs in mock mode by default.

The configuration is:

MOCK_LLM = os.getenv("MOCK_LLM", "1")

Therefore, if MOCK_LLM is not set, the application uses mock mode.

Mock mode does not require:

An external LLM API
An API key
An external LLM provider

The following components still work normally:

Embedding generation
ChromaDB storage
ChromaDB retrieval
LangGraph routing
Pydantic validation
FastAPI

Only the final LLM generation step is mocked.

10. Pydantic Output Schema

The final response is validated using Pydantic.

The response contains three fields:

{
  "answer": "string",
  "sources": ["string"],
  "confidence": 1.0
}

The confidence value must be between 0.0 and 1.0.

In mock mode, the confidence is set to:

1.0

For policy questions, sources contains the retrieved document IDs.

For general questions, sources is an empty list.

11. FastAPI

The FastAPI application is implemented in:

main.py

The main API endpoint is:

POST /ask
Request
{
  "query": "What is the delivery fee for orders below INR 149?"
}
Response
{
  "answer": "Based on the retrieved context: ...",
  "sources": [
    "doc_01",
    "doc_05",
    "doc_03"
  ],
  "confidence": 1.0
}
12. Running FastAPI

Activate the virtual environment:

.\.venv\Scripts\Activate.ps1

Start the FastAPI server:

uvicorn main:app --reload

The API runs locally at:

http://127.0.0.1:8000

Interactive Swagger documentation is available at:

http://127.0.0.1:8000/docs
13. API Testing
Test 1: Policy Question
Request
{
  "query": "What is the delivery fee for orders below INR 149?"
}
Result

The query was classified as:

policy

The system retrieved documents from ChromaDB.

During testing, the retrieved documents were:

doc_01
doc_05
doc_03

The API returned an answer beginning with:

Based on the retrieved context: Zepto delivers grocery and household essentials...

The request completed successfully with HTTP status:

200 OK
Test 2: General Question
Request
{
  "query": "What is the capital of India?"
}
Response
{
  "answer": "I can only answer questions about Zepto policies right now.",
  "sources": [],
  "confidence": 1.0
}

The query was classified as:

general

No retrieval was performed for this question.

14. End-to-End Data Flow

The complete application flow is:

1. Zepto Policy Documents
          |
          v
2. ingest.py
          |
          v
3. Sentence Transformer
   all-MiniLM-L6-v2
          |
          v
4. ChromaDB
   zepto_policies
          |
          v
5. User Query
          |
          v
6. FastAPI /ask
          |
          v
7. LangGraph
          |
          v
8. classify_intent
       /       \
      /         \
 policy        general
   |              |
   v              v
retrieve       direct_answer
   |
   v
Top 3 documents
   |
   v
Mock answer
   |
   v
Pydantic validation
   |
   v
FastAPI JSON response


15. Component Responsibilities
Component	Responsibility
docs/	Stores Zepto policy documents
ingest.py	Loads documents and creates embeddings
Sentence Transformer	Converts text into embeddings
ChromaDB	Stores embeddings and performs similarity search
prompt.py	Defines the structured prompt
graph.py	Implements LangGraph workflow
classify_intent	Classifies policy/general queries
retrieve_and_answer	Retrieves top 3 policy documents
direct_answer	Handles general questions
Pydantic	Validates output
main.py	Exposes FastAPI API
Dockerfile	Defines container configuration
16. Installation and Running
Step 1: Create virtual environment
python -m venv .venv
Step 2: Activate virtual environment
.\.venv\Scripts\Activate.ps1
Step 3: Install dependencies
pip install -r requirements.txt
Step 4: Run ingestion
python ingest.py
Step 5: Test LangGraph
python graph.py
Step 6: Start FastAPI
uvicorn main:app --reload
Step 7: Open Swagger
http://127.0.0.1:8000/docs
17. Docker

A Dockerfile is included for containerization.

FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 7860

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]

The container is configured to run FastAPI on port 7860.

If Docker is available, the image can be built using:

docker build -t zepto-support-assistant .

The container can be started using:

docker run -p 7860:7860 zepto-support-assistant

The API can then be accessed at:

http://localhost:7860/docs

Docker was not executed locally during development because Docker Desktop was not installed on the development laptop.

18. Limitations

The current implementation uses mock mode by default.

Therefore:

The final answer generation is deterministic.
The intent classifier uses keyword-based classification.
General questions receive a fixed response.
Policy retrieval is performed using real embeddings and ChromaDB.
The optional real-LLM integration is not enabled in the default configuration.
Docker configuration is included but was not locally executed.
19. Conclusion

This project demonstrates an end-to-end RAG-based Zepto customer support assistant.

The system:

Loads Zepto policy documents.
Generates local embeddings using Sentence Transformers.
Stores the embeddings in ChromaDB.
Retrieves relevant policy documents using cosine similarity.
Uses LangGraph to classify and route user questions.
Validates responses using Pydantic.
Exposes the application through FastAPI.
Includes a Dockerfile for containerization.

The application can run in mock mode without requiring an external LLM API key.

