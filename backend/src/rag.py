"""Main RAG module. Implements the functionality for RAG (Database, LLM)"""
from backend.src.embedding import get_embedding_model
from backend.src.database import get_knowledge_base
from backend.src.config import EMBEDDING_MODEL_NAME, DATASET_NAME, DEVICE
from backend.src.llm import LLM
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
        embedding_model.embed_query("Warumup query will warmup the model. Lets gooo!")
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
        prompt_in_chat_format = [
            {
                "role": "system",
                "content": """Using the information contained in the context, give a comprehensive but short answer to the question.
                Answer directly without introduction.
                Respond only to the question asked, response should be concise and relevant to the question. Only use relevant documents.
                In your answer, put the source corresponding to document you used for the answer at the end.
                If the answer cannot be deduced from the context, give the following answer: I am sorry, I could not find an answer to
                your question. Never give an empty query.""",
            },
            {
                "role": "user",
                "content": """
                Context: {context}
                ---
                Sources: {sources}
                ---
                Now here is the question you need to answer.
                Question: {question}""",
            },
        ]
        self.llm = LLM(chat_template=prompt_in_chat_format)
        logger.info("Model loaded, warming model up!")
        self.llm.prompt_model(query="Wakey, wakey, are you ready to give some dope answers?", context="", sources="")
        logger.info("Model is warmed up!")
        logger.info("RAG Setup is done!")
    
    def get_top_k_embeddings(self, query: str, k=5):
        retrieved_docs = self.vector_db_faiss.similarity_search(query=query, k=k)
        #print(retrieved_docs[0].page_content)
        #print(retrieved_docs[0].metadata)
        return retrieved_docs
    
    def format_answers(self, answers: list) -> str:
        output = ""
        for answer in answers:
            output += f"answer: {answer.page_content}, source: {answer.metadata['source']}\n"
        return output


    def response_from_k_embeddings(self, query, k=5) -> str:
        answers = self.get_top_k_embeddings(query, k)
        """formatted_answers = self.format_answers(answers)
        prompt = f"Question: {query}.\nLook at the following possible answers and select relevant of these answers."\
        f"Indicate the extracted relevant parts by putting them into quotation marks and add the source to the selected answer.\n"\
        + formatted_answers
        llm_answer = self.llm.prompt_model(prompt)
        return llm_answer"""
        context = "\nExtracted documents:\n"
        context += "".join([f"Document {str(i)}:::\n" + doc.page_content for i, doc in enumerate(answers)])
        sources = "".join([f"Source {str(i)}:\n" + doc.metadata['source'] for i, doc in enumerate(answers)])
        answer = self.llm.prompt_model(query, context, sources)
        return answer


if __name__ == '__main__':
    rag = RAG()