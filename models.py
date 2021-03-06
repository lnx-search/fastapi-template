from typing import Optional, Dict, List, Union

from datetime import datetime
from pydantic import BaseModel, conint, Field
from enum import Enum


class StorageType(Enum):
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


class FieldDeclaration(BaseModel):
    type: FieldType
    stored: Optional[bool]
    indexed: Optional[bool]
    multi: bool = False
    fast: bool = False


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


class Sort(Enum):
    Acs = "acs"
    Desc = "desc"


class Occur(Enum):
    Should = "should"
    Must = "must"
    MustNot = "mustnot"


class FuzzyKind(BaseModel):
    """ The required context for the fuzzy kind query. """

    ctx: str
    fields: Optional[Union[str, List[str]]]


class NormalKind(BaseModel):
    """ The required context for the normal kind query. """

    ctx: str


class MoreLikeThisKind(BaseModel):
    """ The required context for the normal kind query. """

    ctx: int


class TermKind(BaseModel):
    """ The required context for the term kind query. """

    ctx: str
    fields: Union[str, List[str]]


class QueryData(BaseModel):
    occur: Occur = Occur.Should


class FuzzyQueryData(QueryData):
    fuzzy: FuzzyKind


class NormalQueryData(QueryData):
    normal: NormalKind


class MoreLikeThisQueryData(QueryData):
    more_like_this: MoreLikeThisKind = Field(alias="more-like-this")


class TermQueryData(QueryData):
    term: TermKind


QueryKinds = Union[FuzzyQueryData, NormalQueryData, MoreLikeThisQueryData, TermQueryData]


class QueryPayload(BaseModel):
    query: Union[str, QueryKinds, List[QueryKinds]]
    limit: conint(gt=0) = 20
    offset: conint(ge=0) = 0
    order_by: Optional[str] = None
    sort: Sort = Sort.Desc


class DocumentHit(BaseModel):
    data: Dict[str, Union[List[Union[str, int, float]], str, int, float]]
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


class DocumentFetchResponse(BasicResponse):
    data: DocumentHit


class StopwordsResponse(BasicResponse):
    data: List[str]


class SynonymResponse(BasicResponse):
    data: Dict[str, List[str]]