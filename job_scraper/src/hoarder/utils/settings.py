from pydantic_settings import BaseSettings, SettingsConfigDict
import os
from typing import Annotated
from pydantic import Field


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=os.path.join(os.path.dirname(__file__) ,'../../.env'), env_file_encoding='utf-8', case_sensitive=False)


    db_url: Annotated[str, Field(default="")]
    llm_provider: Annotated[str, Field(default="openai")]
    openai_key: Annotated[str, Field(alias="openai_api_key", default="")]

settings = Settings()