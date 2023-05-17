from dotenv import load_dotenv
from pydantic import BaseSettings, Field


load_dotenv()


class DBSettings(BaseSettings):
    db_url: str = Field(env="DATABASE_URL", default="mongodb://user:pass@localhost:6000/ugc?authSource=admin")
    db_name: str = Field(env="MONGO_INITDB_DATABASE", default="ugc")

    class Config:
        env_file: str = ".env"
        env_file_encoding: str = "utf-8"


db_settings = DBSettings()
