from typing import Optional, Dict, List, Union

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
    boost_fields: Dict[str, str]

    reader_threads: conint(gt=0) = 1
    max_concurrency: conint(gt=1)

    writer_buffer: conint(ge=300_000)
    writer_threads: conint(gt=0)

    set_conjunction_by_default: bool = False
    use_fast_fuzzy: bool = False
    strip_stop_words: bool = False


class IndexCreationPayload(BaseModel):
    override_if_exists: bool = False
    index: IndexDeclaration


class BasicResponse(BaseModel):
    status: int
    data: Union[str, dict]

