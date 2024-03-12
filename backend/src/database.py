from backend.src.config import EMBEDDING_MODEL_NAME, MARKDOWN_SEPARATORS, CHUNK_SIZE
from langchain.text_splitter import RecursiveCharacterTextSplitter
from transformers import AutoTokenizer
from typing import Optional
from langchain.docstore.document import Document as LangchainDocument
from tqdm import tqdm
import pandas as pd
import matplotlib.pyplot as plt
from langchain_community.vectorstores import FAISS
from langchain_community.vectorstores.utils import DistanceStrategy
from langchain_community.embeddings import HuggingFaceEmbeddings


def split_documents(
    chunk_size: int,
    knowledge_base: list[LangchainDocument],
    tokenizer_name: Optional[str] = EMBEDDING_MODEL_NAME,  # onyl needed to get the right tokenizer
) -> list[LangchainDocument]:
    """
    Split documents into chunks of maximum size `chunk_size` tokens and return a list of documents.

    Chunks should be small enough for the model to find relevant content easily
    We use recursive chunking to preserve the semantics of the text
    We use a hierarchical list of separators specifically tailored for splitting Markdown documents
    """
    text_splitter = RecursiveCharacterTextSplitter.from_huggingface_tokenizer(
        AutoTokenizer.from_pretrained(tokenizer_name),
        chunk_size=chunk_size,
        chunk_overlap=int(chunk_size / 10),
        add_start_index=True,
        strip_whitespace=True,
        separators=MARKDOWN_SEPARATORS,
        is_separator_regex=True
    )

    docs_processed = []
    for doc in knowledge_base:
        docs_processed += text_splitter.split_documents([doc])

    # Remove duplicates
    unique_texts = {}
    docs_processed_unique = []
    for doc in docs_processed:
        if doc.page_content not in unique_texts:
            unique_texts[doc.page_content] = True
            docs_processed_unique.append(doc)

    return docs_processed_unique


def visualize_split_lengths():
    # Let's visualize the chunk sizes we would have in tokens from a common model
    tokenizer = AutoTokenizer.from_pretrained(EMBEDDING_MODEL_NAME)
    lengths = [len(tokenizer.encode(doc.page_content)) for doc in tqdm(docs_processed)]
    fig = pd.Series(lengths).hist()
    plt.title("Distribution of document lengths in the knowledge base (in count of tokens)")
    plt.show()

def get_knowledge_base(embedding_model: HuggingFaceEmbeddings, dataset):
    """Function to get the FAISS knowledge base of the embedded texts.

    Args:
        embedding_model (HuggingFaceEmbeddings): Model to embed the data

    Returns:
        _type_: FAISS database for querying
    """
    # This list is taken from LangChain's MarkdownTextSplitter class.
    # test database, should be enough for now
    raw_knowledge_base = [
        LangchainDocument(page_content=doc["text"], metadata={"source": doc["source"]}) for doc in tqdm(dataset)
    ]
    #raw_knowledge_base = raw_knowledge_base[:10]
    print("Splitting Documents")
    docs_processed = split_documents(
        CHUNK_SIZE,  # We choose a chunk size adapted to our model
        raw_knowledge_base,
        tokenizer_name=EMBEDDING_MODEL_NAME,
    )
    print("Generating Embeddings")
    return FAISS.from_documents(
        docs_processed, embedding_model, distance_strategy=DistanceStrategy.COSINE
    )