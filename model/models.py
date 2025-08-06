from pydantic import BaseModel, RootModel, Field
from typing import Optional, List, Dict, Any, Union

class Metadata(BaseModel):
    Summary: List[str]
    Title: str
    Author: str
    DateCreated: str
    LastModifiedDate: str
    Publishier: str
    Language: str
    PageCount: Union[int,str]
    SentimentTone: str

class ChangeFormat(BaseModel):
    Page: str
    Changes: str

class SummaryResponse(RootModel[list[ChangeFormat]]):
    pass
