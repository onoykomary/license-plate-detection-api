from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    MODEL_PATH: str
    CONF_THRESHOLD: float = 0.25
    IMG_SIZE: int = 800

    REDIS_URL: str
    BROKER_URL: str
    SQLALCHEMY_DATABASE_URL: str

    S3_ENDPOINT_URL: str
    S3_ACCESS_KEY: str
    S3_SECRET_KEY: str
    S3_BUCKET_NAME: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
