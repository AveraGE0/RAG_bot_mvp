"""Main RAG module. Implements the functionality for RAG (Database, LLM)"""
from backend.src.embedding import get_embedding_model
from backend.src.database import get_knowledge_base
from backend.src.config import EMBEDDING_MODEL_NAME, DATASET_NAME
import datasets
import torch
import logging

logging.basicConfig(filename='logs/app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level=logging.INFO)


# Get the logger specified in the file
logger = logging.getLogger(__name__)


class RAG():
    def __init__(self) -> None:
        logger.info(f"String Rag, using cuda:{ torch.cuda.is_available()}, torch version: {torch.__version__}")
        logger.info(f"loading model {EMBEDDING_MODEL_NAME}")
        embedding_model = get_embedding_model(EMBEDDING_MODEL_NAME)
        logger.info(f"Warming up model")
        embedding_model.embed_query("Warumup query will warmup the model. Lets gooo!")
        logger.info(f"Warmup done!")
        logger.info(f"Loading dataset: {DATASET_NAME}")
        # test dataset from hugging face
        ds = datasets.load_dataset(DATASET_NAME, split="train")
        ds = datasets.load_dataset("csv", data_files="./data/vu_dataset.csv", split="train")
        logger.info("Setting up vector database (FAISS)")
        self.vector_db_faiss = get_knowledge_base(embedding_model, ds)
        logger.info("RAG Setup is done!")
    
    def get_top_k_embeddings(self, query: str, k=5):
        retrieved_docs = self.vector_db_faiss.similarity_search(query=query, k=k)
        #print(retrieved_docs[0].page_content)
        #print(retrieved_docs[0].metadata)
        return retrieved_docs


if __name__ == '__main__':
    rag = RAG()