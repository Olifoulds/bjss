"""
This module integrates Azure OpenAI services with Elasticsearch to index documents,
perform similarity searches, and generate responses using a GPT model.
"""

import os
from uuid import uuid4

from langchain_core.documents import Document
from langchain_elasticsearch import ElasticsearchStore
from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings

openai_api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2023-12-01-preview")

embeddings = AzureOpenAIEmbeddings(
    model="text-embedding-3-large",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    openai_api_version=openai_api_version,
    chunk_size=10,
)

llm = AzureChatOpenAI(
    azure_deployment="gpt-4o",
    openai_api_version=openai_api_version,
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)


def get_vector_store():
    """
    Initializes and returns an ElasticsearchStore instance configured with Azure OpenAI
    embeddings and connection parameters.

    References:
        https://python.langchain.com/v0.2/docs/integrations/vectorstores/elasticsearch/

    Returns:
        ElasticsearchStore: An instance connected to the specified Elasticsearch index.
    """
    return ElasticsearchStore(
        es_url=os.getenv("ES_URL"),
        index_name="openai_kb_index",
        embedding=embeddings,
        es_user="elastic",
        es_password=os.getenv("ES_PASSWORD"),
    )


def index_doc(filename, content):
    """
    Indexes a single document into Elasticsearch with generated UUID.

    Args:
        filename (str): The name of the source file.
        content (str): The textual content of the document.

    References:
        https://python.langchain.com/v0.2/docs/integrations/vectorstores/elasticsearch/#add-items-to-vector-store
        https://api.python.langchain.com/en/latest/documents/langchain_core.documents.base.Document.html

    Returns:
        list: A list containing the UUID of the indexed document.
    """
    document = Document(page_content=content, metadata={"source": filename})
    documents = [document]
    uuids = [str(uuid4()) for _ in range(len(documents))]
    vector_store = get_vector_store()
    vector_store.add_documents(documents=documents, ids=uuids)
    return uuids


def search(query):
    """
    Performs a similarity search on the indexed documents using the provided
    query and generates a response using a GPT model.

    Args:
        query (str): The search query string.

    References:
        https://api.python.langchain.com/en/latest/llms/langchain_community.llms.openai.AzureOpenAI.html
        https://python.langchain.com/v0.2/docs/integrations/llms/azure_openai/

    Returns:
        list: A list of tuples containing the generated response and its corresponding
        similarity score.
    """
    vector_store = get_vector_store()
    vector_store_matches = vector_store.similarity_search_with_score(
        query=query,
        k=5,
    )

    # This return is for the initial state with simple nearest-neighbour searches
    return vector_store_matches

    # Workshop Task: Now that we have our responses from the vector store
    #                We would like to extend the code sufficiently that it takes one/some matches
    #                structures them in to a neat prompt message and invokes the Azure OpenAI LLM.
    #                You may need to structure the return to match the object vector_store_matches
    #                was previously returning (or modify the app.py and templates/search.html)


    # Declare variables for the document and the confidence score for the first supplied document


    # Construct a formatted message to send to the LLM following the documentation


    # Declare a variable for the response when invoking the LLM with the crafted prompt


    # Declare a variable to structure the response and return it
    # You might want to structure the return value like:
    #   list(tuple(dict{"page_content": string},int))

