"""Main RAG module. Implements the functionality for RAG (Database, LLM)"""
from backend.src.embedding import get_embedding_model
from backend.src.database import get_knowledge_base
from backend.src.config import EMBEDDING_MODEL_NAME
import datasets


def rag():
    embedding_model = get_embedding_model(EMBEDDING_MODEL_NAME)
    # test dataset from hugging face
    ds = datasets.load_dataset("m-ric/huggingface_doc", split="train")
    vecotr_db_faiss = get_knowledge_base(embedding_model, ds)

    # test the querying
    user_query = input("Give test query:")
    print(f"\nStarting retrieval for {user_query=}...")
    retrieved_docs = vecotr_db_faiss.similarity_search(query=user_query, k=5)
    print("\n==================================Top document==================================")
    print(retrieved_docs[0].page_content)
    print("==================================Metadata==================================")
    print(retrieved_docs[0].metadata)