import os
import sys
import json
from dotenv import load_dotenv
from utils.config_loader import load_config
from logger.custom_logger import CustomLogger

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_groq import ChatGroq
from exeption.custom_exeption import DocumentPortalExeption
log = CustomLogger().get_logger(__name__)

class ApiKeyManager:
    REQUIRED_KEYS = ["GROQ_API_KEY","GOOGLE_API_KEY"]

    def __init__(self):
        self.api_keys = {}
        raw = os.getenv("API_KEYS")

        if raw:
            try:
                parsed = json.loads(raw)
                if not isinstance(parsed,dict):
                    raise ValueError("API_KEYS is not a valid JSON object")
                self.api_keys = parsed
                log.info("Loaded API_KEYS from ECS secret")
            except Exception as e:
                log.warning("Failed to parse API_KEYS as JSON", error=str(e))
        
        for key in self.REQUIRED_KEYS:
            if not self.api_keys.get(key):
                env_val = os.getenv(key)
                if env_val:
                    self.api_keys[key] = env_val
                    log.info(f"Loaded {key} from individual env var")
            
        missing = [k for k in self.REQUIRED_KEYS if not self.api_keys.get(k)]
        if missing:
            log.error("Missing required API KEYS", missing_keys=missing)
            raise DocumentPortalExeption("Missing API Keys", sys)
        log.info("API keys loaded", keys={k: v[:6] + "..." for k, v in self.api_keys.items()})


    def get(self, key: str) -> str:
        val = self.api_keys.get(key)
        if not val:
            raise KeyError(f"API key for {key} is missing")
        return val




class Model_loader:
    def __init__(self):
        if os.getenv("ENV","local").lower() != "production":
            load_dotenv()
            log.info("Running in LOCAL mode: .env loaded")
        else:
            log.info("Running in PRODUCTION mode")
        
        self.api_key_mgr = ApiKeyManager()
        self._validate_env()
        self.config = load_config()
        log.info("Congigure configure succefully", config_keys=list(self.config.keys()))
    def load_embeddings(self):
        try:
            log.info("Loading embedding model...")
            model_name = self.config["embedding_model"]["model_name"]
            return GoogleGenerativeAIEmbeddings(
                model=model_name,
                google_api_key=self.api_key_mgr.get("GOOGLE_API_KEY"))
        except Exception as e:
            log.error("Error loading embedding model", error=str(e))
            raise DocumentPortalExeption("Failed to load embedding models", sys)
        

    def _validate_env(self):
        required_vars = ["GOOGLE_API_KEY", "GROQ_API_KEY"]
        self.api_keys = {key:os.getenv(key) for key in required_vars}
        missing = [k for k,v in self.api_keys.items() if not v]
        if missing:
            log.error("Missing enviroment variables",missing_vars=missing)
            raise DocumentPortalExeption("Missing enviroment variables",sys)
        log.info("Enviroment variables validated", available_keys = [k for k in self.api_keys if self.api_keys[k]])


    def load_llm(self, *args, **kwargs):
        llm_block = self.config["llm"]
        log.info("Loading LLM...")
        provider_key = os.getenv("LLM_PROVIDER","google")
        if provider_key not in llm_block:
            raise ValueError(f"Provider '{provider_key}' not found in config")
        
        llm_config = llm_block[provider_key]
        provider = llm_config.get("provider")
        model_name = llm_config.get("model_name")
        temperature = llm_config.get("temperature",0.2)
        max_tokens = llm_config.get("max_output_tokens", 2048)

        log.info("Loading LLM", provider=provider, model= model_name, temperature = temperature, max_tokens = max_tokens)
        if provider =="google":
            llm = ChatGoogleGenerativeAI(
                model = model_name,
                google_api_key = self.api_key_mgr.get("GOOGLE_API_KEY"),
                temperature = temperature,
                max_tokens = max_tokens
            )
            return llm
        elif provider=="groq":
            llm = ChatGroq(
                model=model_name,
                api_key=self.api_key_mgr.get("GROQ_API_KEY"),
                temperature=temperature,
            )
            return llm
        else:
            log.error("Unsupported LLM provider", provider=provider)
            raise ValueError(f"Unsupported LLM provider:{provider}")


if __name__=="__main__":
    loader = Model_loader()

    embeddings = loader.load_embeddings()
    print(f"Embedding model is loaded: {embeddings}")

    # result = embeddings.embed_query("Hello how are you")
    # print(f"Embedding result: {result}")

    llm = loader.load_llm()
    print(f"LLM Loaded: {llm}")

    #Test model
    result = llm.invoke("Hello how are you")
    print(f"LLM Result: {result.content}")
