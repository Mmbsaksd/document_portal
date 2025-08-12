from pydantic import BaseModel, RootModel, Field
from typing import Optional, List, Dict, Any, Union
from enum import Enum


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

class PromptType(str,Enum):
    DOCUMENT_ANALYSIS = "document_analysis"
    DOCUMENT_COMPARISON = "document_comparison"
    CONTEXTUALIZE_QUESTION = "contextualize_question"
    CONTEXT_QA = "context_qa"


