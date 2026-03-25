from typing import TypedDict, List


# initial input from user, fills out the metadata for the paper
class PaperMetadata(TypedDict):
    title: str
    authors: List[str]
    year: str
