from pydantic_settings import BaseSettings, SettingsConfigDict #tool that makes sure api keys are valid strings
from pathlib import Path #library for finding paths

#cache constants
News_TTL = 86400 #24hrs
Wiki_TTL = 604800 #7days

#Pydantic for parsing api keys and string validation
class Settings(BaseSettings):
    NEWS_API_KEY: str
    ANTHROPIC_API_KEY: str
    #LEVELS_FYI_API_KEY:
    #since this finds a relative path, i used pathlib to find a path to env in the same folder as this file main.py
    model_config = SettingsConfigDict(env_file= Path(__file__).parent / ".env")

# BaseSettings object which holds:
# - ANTHROPIC_API_KEY
# - NEWS_API_KEY
# - LEVELS_FYI_API_KEY
settings = Settings()


