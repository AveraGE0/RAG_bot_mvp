# model for embedding (and used to get tokenizer)
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"  # "thenlper/gte-small"
DATASET_NAME = "m-ric/huggingface_doc"
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

CHUNK_SIZE = 512