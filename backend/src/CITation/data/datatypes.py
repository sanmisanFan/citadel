from typing import TypedDict, List

# TODO: type the rest of the input / output in the pipeline!
# use pydantic to validate?


# initial input from user, fills out the metadata for the paper
class PaperMetadata(TypedDict):
    title: str
    authors: List[str]
    year: str


class ParsedReference(TypedDict):
    authors: list[str]
    title: str
    venue: str | None
    raw_venue: str | None
    year: str | None
    pages: str | None
    arxiv_id: str | None
    doi: str | None
    abstract: str | None
    ref_id: str | int | None
