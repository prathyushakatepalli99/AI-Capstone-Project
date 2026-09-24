from fastapi import FastAPI
from pydantic import BaseModel, Field

from graph import app as support_graph


# ==========================================
# FastAPI application
# ==========================================

app = FastAPI(
    title="Zepto Support Assistant",
    description="RAG-based Zepto policy support assistant",
    version="1.0.0"
)


# ==========================================
# Request schema
# ==========================================

class AskRequest(BaseModel):
    query: str


# ==========================================
# Response schema
# ==========================================

class AskResponse(BaseModel):
    answer: str
    sources: list[str]
    confidence: float = Field(
        ge=0.0,
        le=1.0
    )


# ==========================================
# Health check
# ==========================================

@app.get("/")
def root():

    return {
        "message": "Zepto Support Assistant is running"
    }


# ==========================================
# Ask endpoint
# ==========================================

@app.post(
    "/ask",
    response_model=AskResponse
)
def ask(request: AskRequest):

    result = support_graph.invoke({
        "query": request.query
    })

    return AskResponse(
        answer=result["answer"],
        sources=result["sources"],
        confidence=result["confidence"]
    )