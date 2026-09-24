import os
import chromadb
from sentence_transformers import SentenceTransformer


# -----------------------------------
# 1. Paths
# -----------------------------------

DOCS_FOLDER = "docs"
CHROMA_FOLDER = "chroma_db"


# -----------------------------------
# 2. Load embedding model
# -----------------------------------

print("Loading embedding model...")

model = SentenceTransformer("all-MiniLM-L6-v2")

print("Embedding model loaded.")


# -----------------------------------
# 3. Create ChromaDB client
# -----------------------------------

client = chromadb.PersistentClient(
    path=CHROMA_FOLDER
)


# -----------------------------------
# 4. Create / get collection
# -----------------------------------

collection = client.get_or_create_collection(
    name="zepto_policies",
    metadata={"hnsw:space": "cosine"}
)


# -----------------------------------
# 5. Read documents
# -----------------------------------

documents = []
document_ids = []

for filename in sorted(os.listdir(DOCS_FOLDER)):

    if filename.endswith(".txt"):

        filepath = os.path.join(
            DOCS_FOLDER,
            filename
        )

        with open(
            filepath,
            "r",
            encoding="utf-8"
        ) as file:

            text = file.read().strip()

        documents.append(text)
        document_ids.append(
            filename.replace(".txt", "")
        )


# -----------------------------------
# 6. Create embeddings
# -----------------------------------

print(f"Found {len(documents)} documents.")

embeddings = model.encode(
    documents
).tolist()


# -----------------------------------
# 7. Store in ChromaDB
# -----------------------------------

collection.upsert(
    ids=document_ids,
    documents=documents,
    embeddings=embeddings
)


# -----------------------------------
# 8. Verify
# -----------------------------------

print(
    "Documents stored:",
    collection.count()
)

print("Document IDs:")

for doc_id in document_ids:
    print("-", doc_id)

print("\nIngestion completed successfully!")