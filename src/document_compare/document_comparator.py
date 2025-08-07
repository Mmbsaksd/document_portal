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
        load_dotenv()
        self.log = CustomLogger().get_logger(__name__)
        self.loader = Model_loader()
        self.llm = self.loader.load_llm()
        self.parser = JsonOutputParser(pydantic_object=SummaryResponse)
        self.fixing_parser = OutputFixingParser.from_llm(parser=self.parser, llm = self.llm)
        self. prompt = PROMPT_REGISTRY["document_comparison"]
        self.chain = self.prompt | self.llm | self.fixing_parser
        self.log.info("Document Comparator initialized with model and parser.", sys)



    def compare_documents(self, combined_docs)->pd.DataFrame:
        try:
            inputs = {
                "combined_docs": combined_docs,
                "format_instruction": self.parser.get_format_instructions()
            }
            self.log.info("Starting document comparison.", inputs = inputs)
            response = self.chain.invoke(inputs)
            self.log.info("Document comparison completed.", response=response)
            return self._format_response(response)
        except Exception as e:
            self.log.error(f"Error in compare documents: {e}")
            raise DocumentPortalExeption("An error occured while comparing documents", sys)
    def _format_response(self,response_parsed:list[dict])->pd.DataFrame:
        try:
            df = pd.DataFrame(response_parsed)
            self.log.info("Response Formatted in DataFrame", dataframe=df)
        except Exception as e:
            self.log.error(f"Error formatting response into DataFrame: {e}")
            raise DocumentPortalExeption("Error formating response: ", sys)

