from fastapi import FastAPI

from models import *


def get_md(file: str) -> str:
    with open(f"./docs/{file}.md", encoding="UTF-8") as file:
        return file.read()


INDEXES_TITLE = "📚 Managing indexes"
TRANSACTIONS_TITLE = "💾 Managing transactions"
DOCUMENTS_TITLE = "📃 Managing documents"
SEARCHES_TITLE = "🔍 Run searches"
AUTH_TITLE = "🔑 Securing lnx"
OPTIMISING_TITLE = "⚡ Optimising your index"

lnx = FastAPI(
    version="0.6.0",
    title="Lnx Docs",
    description=get_md("desc"),
    docs_url=None,
    redoc_url="/",
    openapi_tags=[
        {
            "name": INDEXES_TITLE,
            "description": get_md("indexes")
        },
        {
            "name": TRANSACTIONS_TITLE,
            "description": get_md("transactions")
        },
        {
            "name": DOCUMENTS_TITLE,
            "description": get_md("documents")
        },
        {
            "name": SEARCHES_TITLE,
            "description": get_md("searching")
        },
        {
            "name": AUTH_TITLE,
            "description": get_md("auth")
        },
        {
            "name": OPTIMISING_TITLE,
            "description": get_md("documents")
        },
    ]
)


@lnx.post(
    "/indexes",
    name="Create Index",
    tags=[INDEXES_TITLE],
    response_model=BasicResponse,
    responses={
        400: {
            "description": (
                "The index already exists (and override has not been set)"
                " or has been rejected by the engine due to a bad payload."
            ),
            "model": BasicResponse,
        },
        422: {
            "description": (
                "The server was unable to deserialize the payload given."
            ),
            "model": BasicResponse,
        }
    },
    response_description=(
        "A standard response from Lnx, with a simple conformation message."
    )
)
async def create_index(_payload: IndexCreationPayload):
    ...


@lnx.delete(
    "/indexes/{index:str}",
    name="Delete Index",
    tags=[INDEXES_TITLE],
    response_model=BasicResponse,
    responses={
        400: {
            "description": "The index does not exist.",
            "model": BasicResponse,
        },
        422: {
            "description": "This can never happen. (This is a docs issue)",
        }
    },
    response_description=(
        "A standard response from Lnx, with a simple conformation message."
    )
)
async def delete_index(index: str):  # noqa
    ...


@lnx.post(
    "/indexes/{index:str}/commit",
    name="Commit",
    tags=[TRANSACTIONS_TITLE],
    response_model=BasicResponse,
    responses={
        400: {
            "description": "The index does not exist.",
            "model": BasicResponse,
        },
        422: {
            "description": "This can never happen. (This is a docs issue)",
        }
    },
    response_description=(
        "A standard response from Lnx, with a simple conformation message."
    )
)
async def commit_changes(index: str):  # noqa
    """
    Finalises any changes to the index documents
    since the last commit and saves them.
    """


@lnx.post(
    "/indexes/{index:str}/rollback",
    name="Rollback",
    tags=[TRANSACTIONS_TITLE],
    response_model=BasicResponse,
    responses={
        400: {
            "description": "The index does not exist.",
            "model": BasicResponse,
        },
        422: {
            "description": "This can never happen. (This is a docs issue)",
        }
    },
    response_description=(
        "A standard response from Lnx, with a simple conformation message."
    )
)
async def rollback_changes(index: str):  # noqa
    """
    Reverts any changes to the index documents since the
    last commit.
    """


@lnx.post(
    "/indexes/{index:str}/documents",
    name="Add Documents",
    tags=[DOCUMENTS_TITLE],
    response_model=BasicResponse,
    responses={
        400: {
            "description": "The index does not exist.",
            "model": BasicResponse,
        },
        422: {
            "description": (
                "The server was unable to deserialize the payload given."
            ),
            "model": BasicResponse,
        }
    },
    response_description=(
        "A standard response from Lnx, with a simple conformation message."
    )
)
async def add_documents(
    index: str,  # noqa
    payload: Union[Dict[str, Union[List[str], str]], List[Dict[str, Union[List[str], str]]]],  # noqa
):
    """
    Adding a document is relatively simple, you can either add a single document
    represented as a JSON object or you can submit a array of object.

    Every document is checked for the required fields,
    if any docs are missing fields the *entire* request is rejected.
    """
    ...


@lnx.delete(
    "/indexes/{index:str}/documents",
    name="Delete Specific Documents",
    tags=[DOCUMENTS_TITLE],
    response_model=BasicResponse,
    responses={
        400: {
            "description": "The index does not exist.",
            "model": BasicResponse,
        },
        422: {
            "description": (
                "The server was unable to deserialize the payload given."
            ),
            "model": BasicResponse,
        }
    },
    response_description=(
        "A standard response from Lnx, with a simple conformation message."
    ),
)
async def delete_documents(
    index: str,  # noqa
    payload: Union[Dict[str, Union[List[str], str]], List[Dict[str, Union[List[str], str]]]],  # noqa
):
    """
    Docs can only be deleted via terms, it's up to you to make sure a given term is
    unique otherwise multiple docs can be deleted via this method.

    NOTE: This only works with fast fields, so it's a good idea to make a unique
    id or use the document_id via the `_id` field.
    """


@lnx.delete(
    "/indexes/{index:str}/documents/clear",
    name="Clear All Documents",
    tags=[DOCUMENTS_TITLE],
    response_model=BasicResponse,
    responses={
        400: {
            "description": "The index does not exist.",
            "model": BasicResponse,
        },
        422: {
            "description": "This can never happen. (This is a docs issue)",
        }
    },
    response_description=(
        "A standard response from Lnx, with a simple conformation message."
    )
)
async def clear_delete_documents(index: str):  # noqa
    """
    All docs can be cleared from the index via this endpoint.
    """


@lnx.get(
    "/indexes/{index:str}/documents/{document_id:int}",
    name="Get Document By Id",
    tags=[DOCUMENTS_TITLE],
    response_model=BasicResponse,
    responses={
        400: {
            "description": "The index does not exist or the document does not exit.",
            "model": BasicResponse,
        },
        422: {
            "description": "This can never happen. (This is a docs issue)",
        }
    },
    response_description=(
        "A standard response from Lnx, with a simple conformation message."
    )
)
async def get_document(index: str, document_id: int):  # noqa
    """
    Get a single document from the index with it's given document_id.
    """


@lnx.post(
    "/indexes/{index:str}/search",
    name="Search Index",
    tags=[SEARCHES_TITLE],
    response_model=QueryResponse,
    responses={
        400: {
            "description": "The index does not exist or the query is malformed",
            "model": BasicResponse,
        },
        422: {
            "description": (
                "The server was unable to deserialize the payload given."
            ),
            "model": BasicResponse,
        }
    },
    response_description=(
        "A list of matching results ordered by and sorted according to the passed query."
    )
)
async def search_index(index: str, payload: QueryPayload):  # noqa
    """
    Search the index for the given query.
    """


if __name__ == '__main__':
    import uvicorn
    uvicorn.run("template:lnx", port=8888)