"""
This module provides functionality to extract and process text from PDF and Word documents,
splitting the text into batches of specified word counts.
"""

import itertools

from docx_parser import DocumentParser
from pypdf import PdfReader


def split_string_to_list_of_chunked_words(list_of_words, words_in_chunk):
    """
    Splits a string of words into a list of chunked words.

    Args:
        text (str): The string containing words to be split.
        words_in_chunk (int): The number of words in each chunk.

    Returns:
        list: A list of strings, where each string contains a chunk of words.
    """
    list_of_word_tuples = list(
        itertools.batched(list_of_words.split(" "), words_in_chunk)
    )

    return [" ".join(map(str, x)) for x in list_of_word_tuples]


def get_pdf_text(path):
    """
    Extracts text from a PDF file and splits it into batches of 100 words.

    Args:
        path (str): The file path to the PDF document.

    Returns:
        list: A list of strings, where each string contains a batch of 100 words from the PDF text.
    """
    reader = PdfReader(path)
    page_text = ""

    for i in range(len(reader.page_labels)):
        page = reader.pages[i]
        page_text += str(page.extract_text())

    return split_string_to_list_of_chunked_words(page_text, 100)


def get_docx_text(path):
    """
    Extracts text from a Word document and splits it into batches of 100 words.

    Args:
        path (str): The file path to the Word document (.docx).

    Returns:
        list: A list of strings, where each string contains a batch of 100 words
        from the document text.
    """
    doc = DocumentParser(path)
    page_text = ""

    for _type, item in doc.parse():
        if "text" in item:
            page_text += item["text"]

    return split_string_to_list_of_chunked_words(page_text, 100)
