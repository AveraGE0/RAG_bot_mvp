"""Embedding module. Responsible for providing the embedding model"""
from langchain_community.embeddings import HuggingFaceEmbeddings
from sentence_transformers import SentenceTransformer
from backend.src.config import DEVICE


def get_embedding_model(embedding_name: str):
    return HuggingFaceEmbeddings(
        model_name=embedding_name,
        multi_process=False,
        model_kwargs={"device": DEVICE},
        encode_kwargs={"normalize_embeddings": True},  # set True for cosine similarity
    )