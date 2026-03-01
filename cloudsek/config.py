from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    MONGO_URL: str = "mongodb://localhost:27017"
    DB_NAME: str = "metadata_db"


settings = Settings()
