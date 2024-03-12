# model for embedding (and used to get tokenizer)
EMBEDDING_MODEL_NAME = "thenlper/gte-small"
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