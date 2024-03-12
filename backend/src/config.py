# model for embedding (and used to get tokenizer)
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"  # "thenlper/gte-small"
DATASET_NAME = "m-ric/huggingface_doc"
# Split indications for the text splitter
MARKDOWN_SEPARATORS = [
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