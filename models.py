from typing import Optional, Dict, List, Union

from datetime import datetime
from pydantic import BaseModel, conint
from enum import Enum


class StorageType(Enum):
    Memory = "memory"
    TempDir = "tempdir"
    FileSystem = "filesystem"


class FieldType(Enum):
    F64 = "f64"
    U64 = "u64"
    I64 = "i64"
    Date = "date"
    Text = "text"
    String = "string"
    Facet = "facet"


class FastFieldType(Enum):
    Single = "single"
    Multi = "multi"


class FieldDeclaration(BaseModel):
    type: FieldType
    stored: Optional[bool]
    indexed: Optional[bool]
    fast: Optional[FastFieldType]


class IndexDeclaration(BaseModel):
    name: str
    storage_type: StorageType
    fields: Dict[str, FieldDeclaration]
    search_fields: List[str]
    boost_fields: Dict[str, str] = {}

    reader_threads: conint(gt=0) = 1
    max_concurrency: conint(gt=1)

    writer_buffer: Optional[conint(ge=300_000)]
    writer_threads: Optional[conint(gt=0)]

    set_conjunction_by_default: bool = False
    use_fast_fuzzy: bool = False
    strip_stop_words: bool = False
    auto_commit: int = 0


class IndexCreationPayload(BaseModel):
    override_if_exists: bool = False
    index: IndexDeclaration


class QueryKind(Enum):
    """
    The type of query to perform.

    "normal": Uses the Tantivy query parser to produce a query and execute it.
    "fuzzy": Uses typo-tolerant query system, this takes the query as raw text and is not parsed into something else.
    "more-like-this": Searches for documents similar to the given document (document_id).
    "term": Searches for the given query term(s) in the given field(s).
    """
    Normal = "normal"
    Fuzzy = "fuzzy"
    MoreLikeThis = "more-like-this"
    Term: Dict[str, Union[List[Union[str, int, float]], str, int, float]] = {
        "term": "field-name"
    }


class Sort(Enum):
    Acs = "acs"
    Desc = "desc"


class Occur(Enum):
    Should = "should"
    Must = "must"
    MustNot = "mustnot"


class QueryData(BaseModel):
    value: Union[str, int, float]
    kind: QueryKind = QueryKind.Fuzzy
    occur: Occur = Occur.Should


class QueryPayload(BaseModel):
    query: Union[str, QueryData, List[QueryData]]
    limit: conint(gt=0) = 20
    offset: conint(ge=0) = 0
    order_by: Optional[str] = None
    sort: Sort = Sort.Desc


class DocumentHit(BaseModel):
    data: Dict[str, List[str]]
    ratio: Optional[float]
    document_id: str


class QueryResults(BaseModel):
    hits: List[DocumentHit]
    count: int
    time_taken: float


class CreateTokenPayload(BaseModel):
    permissions: int
    user: Optional[str]
    description: Optional[str]
    allowed_indexes: Optional[List[str]]


class TokenData(CreateTokenPayload):
    created: datetime
    token: str


class BasicResponse(BaseModel):
    status: int
    data: Union[str, dict]


class QueryResponse(BasicResponse):
    data: QueryResults


class TokenResponse(BasicResponse):
    data: TokenData
