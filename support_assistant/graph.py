import os
from typing import TypedDict

import chromadb
from sentence_transformers import SentenceTransformer
from pydantic import BaseModel, Field
from langgraph.graph import StateGraph, END

from prompt import build_prompt


# ============================================================
# 1. Configuration
# ============================================================

CHROMA_FOLDER = "chroma_db"
COLLECTION_NAME = "zepto_policies"

MOCK_LLM = os.getenv("MOCK_LLM", "1")


# ============================================================
# 2. Load embedding model
# ============================================================

print("Loading embedding model...")

model = SentenceTransformer("all-MiniLM-L6-v2")

print("Embedding model loaded.")


# ============================================================
# 3. Connect to ChromaDB
# ============================================================

client = chromadb.PersistentClient(
    path=CHROMA_FOLDER
)

collection = client.get_collection(
    name=COLLECTION_NAME
)


# ============================================================
# 4. Output schema
# ============================================================

class AnswerOutput(BaseModel):
    answer: str
    sources: list[str]
    confidence: float = Field(
        ge=0.0,
        le=1.0
    )


# ============================================================
# 5. LangGraph State
# ============================================================

class SupportState(TypedDict, total=False):

    query: str
    intent: str

    answer: str
    sources: list[str]
    confidence: float

    retrieved_chunks: list[str]


# ============================================================
# 6. Node 1 - Classify Intent
# ============================================================

def classify_intent(state: SupportState):

    query = state["query"].lower()

    policy_keywords = [
        "delivery",
        "return",
        "refund",
        "membership",
        "tracking",
        "cancel",
        "gift card",
        "support hours"
    ]

    if any(
        keyword in query
        for keyword in policy_keywords
    ):
        intent = "policy"
    else:
        intent = "general"

    print(f"Intent classified as: {intent}")

    return {
        "intent": intent
    }


# ============================================================
# 7. Node 2 - Retrieve and Answer
# ============================================================

def retrieve_and_answer(state: SupportState):

    query = state["query"]

    # ----------------------------------------
    # Create query embedding
    # ----------------------------------------

    query_embedding = model.encode(
        [query]
    ).tolist()

    # ----------------------------------------
    # Retrieve top 3 documents
    # ----------------------------------------

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=3
    )

    retrieved_documents = results["documents"][0]
    retrieved_ids = results["ids"][0]

    print("\nRetrieved documents:")

    for doc_id in retrieved_ids:
        print("-", doc_id)

    # ----------------------------------------
    # Save retrieved chunks
    # ----------------------------------------

    retrieved_chunks = retrieved_documents

    # ----------------------------------------
    # Mock LLM mode
    # ----------------------------------------

    if MOCK_LLM != "0":

        top_chunk = retrieved_documents[0]

        # First ~200 characters
        snippet = top_chunk[:200]

        answer = (
            "Based on the retrieved context: "
            + snippet
        )

    # ----------------------------------------
    # Optional real LLM mode
    # ----------------------------------------

    else:

        context = "\n\n".join(
            retrieved_documents
        )

        prompt = build_prompt(
            question=query,
            context=context
        )

        # Real LLM integration can be added here.
        # For now we raise a clear message instead
        # of silently making an external API call.

        raise RuntimeError(
            "MOCK_LLM=0 requires a real LLM provider configuration."
        )

    # ----------------------------------------
    # Validate output
    # ----------------------------------------

    validated = AnswerOutput(
        answer=answer,
        sources=retrieved_ids,
        confidence=1.0
    )

    return {
        "answer": validated.answer,
        "sources": validated.sources,
        "confidence": validated.confidence,
        "retrieved_chunks": retrieved_chunks
    }


# ============================================================
# 8. Node 3 - Direct Answer
# ============================================================

def direct_answer(state: SupportState):

    if MOCK_LLM != "0":

        answer = (
            "I can only answer questions about "
            "Zepto policies right now."
        )

    else:

        raise RuntimeError(
            "MOCK_LLM=0 requires a real LLM provider configuration."
        )

    validated = AnswerOutput(
        answer=answer,
        sources=[],
        confidence=1.0
    )

    return {
        "answer": validated.answer,
        "sources": validated.sources,
        "confidence": validated.confidence
    }


# ============================================================
# 9. Conditional Routing
# ============================================================

def route_intent(state: SupportState):

    if state["intent"] == "policy":
        return "retrieve_and_answer"

    return "direct_answer"


# ============================================================
# 10. Build LangGraph
# ============================================================

workflow = StateGraph(SupportState)


workflow.add_node(
    "classify_intent",
    classify_intent
)

workflow.add_node(
    "retrieve_and_answer",
    retrieve_and_answer
)

workflow.add_node(
    "direct_answer",
    direct_answer
)


# Start → classify

workflow.set_entry_point(
    "classify_intent"
)


# Classify → policy/general

workflow.add_conditional_edges(
    "classify_intent",
    route_intent,
    {
        "retrieve_and_answer": "retrieve_and_answer",
        "direct_answer": "direct_answer"
    }
)


# End points

workflow.add_edge(
    "retrieve_and_answer",
    END
)

workflow.add_edge(
    "direct_answer",
    END
)


# ============================================================
# 11. Compile Graph
# ============================================================

app = workflow.compile()


# ============================================================
# 12. Test the Graph
# ============================================================

if __name__ == "__main__":

    print("\n==============================")
    print("Testing policy question")
    print("==============================")

    result = app.invoke({
        "query": "What is the delivery fee below INR 149?"
    })

    print("\nFinal result:")
    print(result)


    print("\n==============================")
    print("Testing general question")
    print("==============================")

    result = app.invoke({
        "query": "What is the capital of India?"
    })

    print("\nFinal result:")
    print(result)