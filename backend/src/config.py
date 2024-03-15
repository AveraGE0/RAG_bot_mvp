import torch
from pathlib import Path
# model for embedding (and used to get tokenizer)
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"  # "thenlper/gte-small"
LLM_MODEL_NAME = "mistralai/Mistral-7B-v0.1"
# if the dataset is custom, make it a path, otherwise it will be looked up online
DATASET_NAME = Path("./data/vu_dataset.csv")  # "m-ric/huggingface_doc"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
# Split indications for the text splitter
MARKDOWN_SEPARATORS = [
    "[1-9].*",
    "[a-z].*",
    "\n#{1,6} ",
    "```\n",
    "\n\\*\\*\\*+\n",
    "\n---+\n",
    "\n___+\n",
    "\n\n",
    "\n",
    " ",
    "",
]
LLM_URL = "http://127.0.0.1:11434/api/generate"
CHUNK_SIZE = 512
MAX_NEW_TOKENS = 1000