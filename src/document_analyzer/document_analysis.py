import os
import sys
from utils.model_loader import Model_loader
from logger.custom_logger import CustomLogger
from exeption.custom_exeption import DocumentPortalExeption
from model.models import *
from langchain_core.output_parsers import JsonOutputParser
from langchain.output_parsers import OutputFixingParser
from prompt.prompt_library import PROMPT_REGISTRY

class DocumentAnalyzer:
    def __init__(self):
        self.log = CustomLogger().get_logger(__name__)
        try:
            self.loader = Model_loader()
            self.llm = self.loader.load_llm()
            

            self.parser = JsonOutputParser(pydantic_object=Metadata)
            self.fixing_parser = OutputFixingParser.from_llm(parser=self.parser, llm = self.llm)
            self.prompt = PROMPT_REGISTRY["documentanalysis"]
            self.log.info("Document Anylyzer initialized successfully")
        except Exception as e:
            self.log.error(f"Error initializing DocumentAnalyzer: {e}")
            raise DocumentPortalExeption("Error in DocumentAnalyzer initialization",sys)

    def analyze_document(self, document_text:str)->dict:
        try:
            chain = self.prompt | self.llm | self.fixing_parser
            self.log.info("Meta data analysis chain initialized")
            
            response = chain.invoke({
                "format_instructions": self.parser.get_format_instructions(),
                "document_text": document_text
            })
            self.log.info("MetaData extraction successful", keys=list(response.keys()))
            return response
        except Exception as e:
            self.log.error("Metadata analysis failed", error=str(e))
            raise DocumentPortalExeption("Metadata extraction failed") from e