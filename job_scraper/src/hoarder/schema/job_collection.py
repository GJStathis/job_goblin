from pydantic import BaseModel


class JobPageRequest(BaseModel):
    url: str
    page_html: str


class JobPageResponse(BaseModel):
    page_id: int
    url: str
    message: str


class JobPageItem(BaseModel):
    page_id: int
    url: str


class JobPageListResponse(BaseModel):
    total: int
    pages: list[JobPageItem]
