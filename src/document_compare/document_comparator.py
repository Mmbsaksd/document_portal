import sys
from dotenv import load_dotenv
import pandas as pd
from logger.custom_logger import CustomLogger
from exeption.custom_exeption import DocumentPortalExeption
from model.models import *
from prompt.prompt_library import PROMPT_REGISTRY
from utils.model_loader import Model_loader
from langchain_core.output_parsers import JsonOutputParser
from langchain.output_parsers import OutputFixingParser

class DocumentComparatorLLM:
    def __init__(self):
        pass
    def compare_documents(self):
        pass
    def _format_response(self):
        pass

