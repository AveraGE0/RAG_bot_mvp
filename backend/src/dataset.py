# this is the pymupdf package
import os
import fitz
import pandas as pd
from pathlib import Path
from datasets import load_dataset


def get_pdf_contents(document_path: Path) -> str:
    """Gets the text contents from a pdf file.

    Args:
        document_path (Path): Path to the pdf file in the filesystem 

    Returns:
        str: The combined text of the pdf as a single string
    """
    doc = fitz.open(document_path) # open a document
    text = ""
    for page in doc: # iterate the document pages
        text += page.get_text()
    return text


def get_pdf_source(document_path: Path, metadata: pd.DataFrame) -> str:
    """Gets the source of a pdf file, if there is one.
    Otherwise the pdf name will be returned.

    Args:
        document_path (Path): path to the document
        metadata (pd.DataFrame): DataFrame with the metadata

    Returns:
        str: A single string representing the source of the document
    """
    return metadata.loc[document_path.name, "source"]


def parse_pdf_files(dir_path: Path) -> pd.DataFrame:
    """Function that reads all texts from a dir that are pdfs,
    adds a source (if there is one) and combines it into a pandas df.

    Args:
        dir_path (Path): path to the pdf files

    Returns:
        pd.DataFrame: Database with pdf content and source
    """
    df_metadata = pd.read_csv(dir_path / "metadata.csv")
    df_metadata = df_metadata.set_index("name")
    contents = []
    sources = []
    for path in [path for path in os.listdir(dir_path) if path.endswith(".pdf")]:
        pdf_path = dir_path / path
        contents.append(get_pdf_contents(pdf_path))
        sources.append(get_pdf_source(pdf_path, df_metadata))
    return pd.DataFrame({"text": contents, "source": sources})


if __name__ == '__main__':
    df_pdf = parse_pdf_files(Path("./data"))
    df_pdf.to_csv("./data/vu_dataset.csv", index=False)
    dataset = load_dataset("csv", data_files="./data/vu_dataset.csv")