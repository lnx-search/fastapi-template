from fastapi import FastAPI, Body

from models import *


def get_md(file: str) -> str:
    with open(f"./docs/{file}.md", encoding="UTF-8") as file:
        return file.read()


INDEXES_TITLE = "📚 Managing indexes"
SNAPSHOTS_TITLE = "📷 Snapshots"
TRANSACTIONS_TITLE = "💾 Managing transactions"
DOCUMENTS_TITLE = "📃 Managing documents"
SEARCHES_TITLE = "🔍 Run searches"
AUTH_TITLE = "🔑 Securing lnx"
OPTIMISING_TITLE = "⚡ Optimising your index"
CONFIG_TITLE = "⚙️ Synonyms & Stopwords"

PERMISSIONS_RESPONSE = {
    401: {
        "description": (
            "You lack the permissions to run this operation."
        ),
        "model": BasicResponse,
    },
}

lnx = FastAPI(
    version="0.8.0",
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
            "name": SNAPSHOTS_TITLE,
            "description": get_md("snapshots")
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
            "name": CONFIG_TITLE,
            "description": get_md("synonyms_and_stopwords")
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
            "description": get_md("optimising")
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
        },
        **PERMISSIONS_RESPONSE,
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
        },
        **PERMISSIONS_RESPONSE,
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
        },
        **PERMISSIONS_RESPONSE,
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
        },
        **PERMISSIONS_RESPONSE,
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
        },
        **PERMISSIONS_RESPONSE,
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


class DeletePayload(BaseModel):
    num_deleted: int
    detail: str


class DeleteResponse(BasicResponse):
    data: DeletePayload


@lnx.delete(
    "/indexes/{index:str}/documents",
    name="Delete Specific Documents",
    tags=[DOCUMENTS_TITLE],
    response_model=DeleteResponse,
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
        },
        **PERMISSIONS_RESPONSE,
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
    id or use the document specific removal via `DELETE /index/:index/document/:document_id`.
    """


@lnx.delete(
    "/indexes/{index:str}/documents/query",
    name="Delete Documents By Query",
    tags=[DOCUMENTS_TITLE],
    response_model=DeleteResponse,
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
        },
        **PERMISSIONS_RESPONSE,
    },
    response_description=(
        "A standard response from Lnx, with a simple conformation message."
    ),
)
async def delete_documents_by_query(
    index: str,  # noqa
    payload: QueryPayload,  # noqa
):
    """
    Deletes any documents matched with the given query.

    This respects the limits and offsets of the query, so to delete all the matched
    results you will need to send the request several time however, This is generally not recommended to do.
    """


@lnx.delete(
    "/indexes/{index:str}/documents/{document_id:int}",
    name="Delete Document",
    tags=[DOCUMENTS_TITLE],
    response_model=BasicResponse,
    responses={
        400: {
            "description": "The index does not exist or the document id is invalid.",
            "model": BasicResponse,
        },
        **PERMISSIONS_RESPONSE,
    },
    response_description=(
        "A standard response from Lnx, with a simple conformation message."
    ),
)
async def delete_documents(
    index: str,  # noqa
    document_id: int,
):
    """
    Delete a specific document with the provided id.
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
        },
        **PERMISSIONS_RESPONSE,
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
    response_model=DocumentFetchResponse,
    responses={
        400: {
            "description": "The index does not exist or the document does not exit.",
            "model": BasicResponse,
        },
        422: {
            "description": "This can never happen. (This is a docs issue)",
        },
        **PERMISSIONS_RESPONSE,
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
        },
        **PERMISSIONS_RESPONSE,
    },
    response_description=(
        "A list of matching results ordered by and sorted according to the passed query."
    )
)
async def search_index(index: str, payload: QueryPayload):  # noqa
    """
    Search the index for the given query.
    """


@lnx.post(
    "/indexes/{index:str}/stopwords",
    name="Add Stopwords",
    tags=[CONFIG_TITLE],
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
        },
        **PERMISSIONS_RESPONSE,
    },
    response_description=(
        "A list of matching results ordered by and sorted according to the passed query."
    )
)
async def add_synonyms(index: str, payload: List[str] = Body(...)):  # noqa
    """
    Adds a set of stopwords to the index.

    Note:
        Stop words are only applied if `strip_stop_words: true` in the schema config.
    """


@lnx.get(
    "/indexes/{index:str}/stopwords",
    name="Get Stopwords",
    tags=[CONFIG_TITLE],
    response_model=StopwordsResponse,
    responses={
        400: {
            "description": "The index does not exist or the query is malformed",
            "model": BasicResponse,
        },
        **PERMISSIONS_RESPONSE,
    },
    response_description=(
        "A "
    )
)
async def get_stopwords(index: str):  # noqa
    """
    Get all the stopwords for the given index.

    This may have unexpected results if no stop words have been added,
    so the engine falls back to a default set of stop words.

    Note:
        Stop words are only applied if `strip_stop_words: true` in the schema config.
    """


@lnx.delete(
    "/indexes/{index:str}/stopwords",
    name="Delete Stopwords",
    tags=[CONFIG_TITLE],
    response_model=BasicResponse,
    responses={
        400: {
            "description": "The index does not exist or the query is malformed",
            "model": BasicResponse,
        },
        **PERMISSIONS_RESPONSE,
    },
)
async def delete_stopwords(index: str, payload: List[str] = Body(...)):  # noqa
    """
    Deletes a set of stopwords from the index.
    """


@lnx.delete(
    "/indexes/{index:str}/stopwords/clear",
    name="Clear All Stopwords",
    tags=[CONFIG_TITLE],
    response_model=BasicResponse,
    responses={
        400: {
            "description": "The index does not exist or the query is malformed",
            "model": BasicResponse,
        },
        **PERMISSIONS_RESPONSE,
    },
)
async def clear_stopwords(index: str):  # noqa
    """
    Deletes all stopwords from the index.
    """


@lnx.post(
    "/indexes/{index:str}/synonyms",
    name="Add Synonyms",
    tags=[CONFIG_TITLE],
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
        },
        **PERMISSIONS_RESPONSE,
    },
    response_description=(
        "A list of matching results ordered by and sorted according to the passed query."
    )
)
async def add_synonyms(index: str, payload: List[str] = Body(...)):  # noqa
    """
    Add synonyms to the index.

    Synonyms can be provided by a array of strings and each entry follows the format of:

    ```
    <word>,<word>:<synonym>,<synonym>,<synonym>
    ```

    Words can be mapped one to one, one to many, or many to many.

    ```json
    [
        "iphone,apple,phone:apple,phone,iphone",
        "oven:microwave,toaster",
        "pen:pencil"
    ]
    ```
    """


@lnx.get(
    "/indexes/{index:str}/synonyms",
    name="Get Synonyms",
    tags=[CONFIG_TITLE],
    response_model=SynonymResponse,
    responses={
        400: {
            "description": "The index does not exist or the query is malformed",
            "model": BasicResponse,
        },
        **PERMISSIONS_RESPONSE,
    },
    response_description=(
        "A JSON object containing keys and their mapped synonyms."
    )
)
async def get_synonyms(index: str):  # noqa
    """
    Get all the synonyms within the index.
    """


@lnx.delete(
    "/indexes/{index:str}/synonyms",
    name="Delete Synonyms",
    tags=[CONFIG_TITLE],
    response_model=BasicResponse,
    responses={
        400: {
            "description": "The index does not exist or the query is malformed",
            "model": BasicResponse,
        },
        **PERMISSIONS_RESPONSE,
    },
)
async def delete_synonyms(index: str, payload: List[str] = Body(...)):  # noqa
    """
    Deletes a set of synonyms from the index.

    Note:
    These delete the word mappings. They do not remove the word from every other word's values.
    i.e. If we have the following synonyms:

    ```json
    [
        "iphone,apple,phone:apple,phone,iphone"
    ]
    ```

    And we delete synonyms with the following payload:
    ```json
    [
        "iphone"
    ]
    ```

    Only the iphone's given synonyms will be removed.
    Meaning both `apple` and `phone` will still have `'apple', 'phone', 'iphone'` as their synonyms.
    """


@lnx.delete(
    "/indexes/{index:str}/synonyms/clear",
    name="Clear All Synonyms",
    tags=[CONFIG_TITLE],
    response_model=BasicResponse,
    responses={
        400: {
            "description": "The index does not exist or the query is malformed",
            "model": BasicResponse,
        },
        **PERMISSIONS_RESPONSE,
    },
)
async def clear_synonyms(index: str):  # noqa
    """
    Deletes all synonyms from the index, essentially making it a blank slate again.
    """


@lnx.post(
    "/auth",
    name="Create Token",
    tags=[AUTH_TITLE],
    response_model=TokenResponse,
    responses={
        422: {
            "description": (
                "The server was unable to deserialize the payload given."
            ),
            "model": BasicResponse,
        },
        **PERMISSIONS_RESPONSE,
    },
    response_description=(
        "A payload containing the response token and other metadata."
    )
)
async def create_token(payload: CreateTokenPayload):  # noqa
    """
    Creates a new access token with a given set of metadata.
    """


@lnx.delete(
    "/auth",
    name="Revoke All Token",
    tags=[AUTH_TITLE],
    response_model=BasicResponse,
    responses={
        422: {
            "description": (
                "The server was unable to deserialize the payload given."
            ),
            "model": BasicResponse,
        },
        **PERMISSIONS_RESPONSE,
    },
    response_description=(
        "A standard conformation message."
    )
)
async def revoke_all_tokens():
    """
    Revoke all access tokens.

    ### WARNING:
    This is absolutely only designed for use in an emergency.
    Running this will revoke all tokens including the super user key,
    run this at your own risk.
    """


@lnx.post(
    "/auth/{token}/revoke",
    name="Revoke Token",
    tags=[AUTH_TITLE],
    response_model=BasicResponse,
    responses={
        400: {
            "description": (
                "The token you provided in the url does not exist."
            ),
            "model": BasicResponse,
        },
        422: {
            "description": "This can never happen. (This is a docs issue)",
        },
        **PERMISSIONS_RESPONSE,
    },
    response_description=(
        "A standard conformation message."
    )
)
async def revoke_token():
    """
    Revokes a given token, any requests after this with the given token
    will be rejected.
    """


@lnx.post(
    "/auth/{token}/edit",
    name="Edit Token",
    tags=[AUTH_TITLE],
    response_model=BasicResponse,
    responses={
        400: {
            "description": (
                "The token you provided in the url does not exist."
            ),
            "model": BasicResponse,
        },
        422: {
            "description": (
                "The server was unable to deserialize the payload given."
            ),
            "model": BasicResponse,
        },
        **PERMISSIONS_RESPONSE,
    },
    response_description=(
        "A payload containing the response token and other metadata."
    )
)
async def edit_token(payload: CreateTokenPayload):  # noqa
    """
    Edits a given token's permissions and metadata.
    The payload will replace **ALL** fields which will either set or unset the
    fields.
    """


if __name__ == '__main__':
    import uvicorn
    uvicorn.run("template:lnx", port=8888)