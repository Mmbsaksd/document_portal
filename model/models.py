from pydantic import BaseModel, Field
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