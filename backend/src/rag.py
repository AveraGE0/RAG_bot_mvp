"""Main RAG module. Implements the functionality for RAG (Database, LLM)"""
from backend.src.embedding import get_embedding_model
from backend.src.database import get_knowledge_base
from backend.src.config import EMBEDDING_MODEL_NAME, DATASET_NAME, DEVICE
import backend.src.logger
import datasets
import torch
import logging
from pathlib import Path

# Get the logger specified in the file
logger = logging.getLogger(__name__)


class RAG():
    def __init__(self) -> None:
        logger.info(f"String Rag, using cuda:{ torch.cuda.is_available()}({DEVICE}), torch version: {torch.__version__}")
        logger.info(f"loading model {EMBEDDING_MODEL_NAME}")
        embedding_model = get_embedding_model(EMBEDDING_MODEL_NAME)
        logger.info(f"Warming up model")
        embedding_model.embed_query("Warm-up query will warmup the model. Lets gooo!")
        logger.info(f"Warmup done!")
        logger.info(f"Loading dataset: {DATASET_NAME}")
        # test dataset from hugging face
        if not isinstance(DATASET_NAME, Path):
            ds = datasets.load_dataset(DATASET_NAME, split="train")
        else:
            ds = datasets.load_dataset("csv", data_files=str(DATASET_NAME), split="train")
        logger.info("Setting up vector database (FAISS)")
        self.vector_db_faiss = get_knowledge_base(embedding_model, ds)
        logger.info("Loading model...")
        self.prompt_in_chat_format = """
                    Context: {context}
                    ---
                    Using only the information contained in the context, give a short answer to the question.
                    Respond only to the question asked, the response should be concise and relevant to the question.
                    In your answer, put the full source link without html tags corresponding to document you used for the answer.
                    Put the links at the end of the answer as a full link to the document.
                    If the answer cannot be deduced from the context, give the following answer: I am sorry, I could not find an answer to
                    your question.

                    Now here is the question you need to answer.
                    Question: {question}
                """
        logger.info("Model loaded, warming model up!")
        logger.info("Model is warmed up!")
        logger.info("RAG Setup is done!")
    
    def get_top_k_embeddings(self, query: str, k=5):
        retrieved_docs = self.vector_db_faiss.similarity_search(query=query, k=k)
        return retrieved_docs    
    
    def get_prompt(self, query: str):
        answers = self.get_top_k_embeddings(query, 5)
        context = "\nExtracted documents:\n"
        context += "".join([
            f"{doc.metadata['source']}:\n {doc.page_content}\n\n" for doc in answers
        ])
        return self.prompt_in_chat_format.format(question=query, context=context)


if __name__ == '__main__':
    rag = RAG()