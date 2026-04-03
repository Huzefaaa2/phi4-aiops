from functools import lru_cache
from pydantic import BaseModel, Field
import os


class Settings(BaseModel):
    ollama_base_url: str = Field(default=os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434"))
    ollama_model: str = Field(default=os.getenv("OLLAMA_MODEL", "phi4:mini"))
    vector_index_path: str = Field(default=os.getenv("VECTOR_INDEX_PATH", "./data/index.faiss"))
    metadata_path: str = Field(default=os.getenv("METADATA_PATH", "./data/index_meta.json"))
    logs_path: str = Field(default=os.getenv("LOGS_PATH", "./data/logs"))
    azure_workspace_id: str = Field(default=os.getenv("AZURE_WORKSPACE_ID", ""))
    azure_tenant_id: str = Field(default=os.getenv("AZURE_TENANT_ID", ""))
    azure_client_id: str = Field(default=os.getenv("AZURE_CLIENT_ID", ""))
    azure_client_secret: str = Field(default=os.getenv("AZURE_CLIENT_SECRET", ""))


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
