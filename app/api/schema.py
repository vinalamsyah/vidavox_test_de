from pydantic import BaseModel
from datetime import datetime


class DocumentsData(BaseModel):
    id: int
    docpath: str
    uploaded_at: datetime


class TextsData(BaseModel):
    id: int
    docid: int
    pagenumber: int
    ordernumber: int
    textvalue: str
    extracted_at: datetime


class EntitiesData(BaseModel):
    id: int
    entityname: str
    entitylabel: str
    docid: int
    pagenumber: int
    ordernumber: int
    startposition: int
    endposition: int
    extracted_at: datetime


class ImagesData(BaseModel):
    id: int
    docid: int
    pagenumber: int
    image: bytes
    imagepath: str
    caption: str | None
    extracted_at: datetime

