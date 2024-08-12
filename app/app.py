"""
This Flask application allows users to upload PDF and Word documents,
process their content into text chunks, index them into an Elasticsearch or
OpenAI-backed search engine, and perform search queries on the indexed content.
"""

import os

from flask import Flask, flash, redirect, render_template, request, url_for
from werkzeug.utils import secure_filename
from .ai import index_doc, search
from .import_file import get_docx_text, get_pdf_text

UPLOAD_FOLDER = os.path.abspath("uploads")
ALLOWED_EXTENSIONS = {"pdf", "doc", "docx"}

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

def allowed_file(filename):
    """
    Checks if a file is allowed based on its extension.

    Args:
        filename (str): The name of the file.

    Returns:
        bool: True if the file extension is allowed, False otherwise.
    """
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/downloads/<name>", methods=["GET", "POST"])
def download_file(name):
    """
    Processes an uploaded file, extracts text, indexes the text in chunks,
    and renders the download page with indexing results.

    Args:
        name (str): The name of the uploaded file.

    Returns:
        str: The rendered template for the download page, displaying the indexing results.
    """
    match os.path.splitext(name)[1]:
        case ".pdf":
            list_of_text_chunks = get_pdf_text(UPLOAD_FOLDER + "/" + name)
        case ".doc":
            list_of_text_chunks = get_docx_text(UPLOAD_FOLDER + "/" + name)
        case ".docx":
            list_of_text_chunks = get_docx_text(UPLOAD_FOLDER + "/" + name)
        case _:
            raise RuntimeError("The file uploaded doesn't have a supported extension")

    vectors = []

    for text_chunk in list_of_text_chunks:
        vectors += index_doc(filename=name, content=text_chunk)

    return render_template("download.html", results=vectors)


@app.route("/search", methods=["POST"])
def search_route():
    """
    Handles search queries and renders the search results page.

    Returns:
        str: The rendered template for the search results page, displaying the search results.
    """
    query = request.form.get("q")
    search_results = search(query=query)
    return render_template("search.html", results=search_results)


@app.route("/", methods=["GET", "POST"])
def upload_file():
    """
    Handles file uploads, validates the file, and redirects to the download page for processing.

    Returns:
        str: The rendered template for the upload page,
        or a redirect to the download page after successful upload.
    """
    if request.method == "POST":
        # check if the post request has the file part
        if "file" not in request.files:
            flash("No file part")
            return redirect(request.url)
        file = request.files["file"]
        # If the user does not select a file, the browser submits an
        # empty file without a filename.

        if file.filename == "":
            flash("No selected file")
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            print(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            return redirect(url_for("download_file", name=filename))

    return render_template("index.html")
