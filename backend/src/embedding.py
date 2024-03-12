"""Embedding module. Responsible for providing the embedding model"""
from langchain_community.embeddings import HuggingFaceEmbeddings


def get_embedding_model(embedding_name: str):
    return HuggingFaceEmbeddings(
        model_name=embedding_name,
        multi_process=True,
        model_kwargs={"device": "cuda"},
        encode_kwargs={"normalize_embeddings": True},  # set True for cosine similarity
    )
