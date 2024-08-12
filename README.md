# ai-knowledge-base-sample
## Pre-Requisites

    - A mechanism for running Docker containers locally, perhaps Docker with Docker Desktop, Rancher, Podman or a preferred alternative
    - The `docker-compose` command being available from your terminal. Depending on your Docker services this maybe built-in or not.
    - Basic familiarity with running Docker containers & Docker-Compose services

## Workshop Tasks

### Setup your local environment

- Run `docker compose up` will start two containers
  - ElasticSearch which is a search and analytics engine, we will be using it as a 'vector store' for our AI
  - Our Knowledge retrieval AI app, which is a simple Python Flask interface.
- Open the [web ui](http://127.0.0.1:8080)

**NOTE** Please be aware that in the interest of keeping this workshop accessible and achievable in a limited time frame the ElasticSearch best practice and security mechanisms have been disabled. This should never be run anywhere but this local development scenario.

### Introducing OpenAI LLM to our base application

- Update the `.env` file with the provided Azure OpenAPI Keys provided
- Modify the `ai.py` file.
  - Modify the `search` function such that it takes the raw matching text from our vector store, and queries the LLM
   to get a natural language response:
   [References](https://python.langchain.com/v0.2/docs/integrations/llms/azure_openai/)

### Further expansion

_If you were unable to complete the previous task or ran out of time, we have a branch with the task completed available_

Discuss what you would do next working towards an enterprise solution.

- Add styling though UI, UX?
- Add support for a conversational workflow?
- Batch uploading of knowledge?
- ...
