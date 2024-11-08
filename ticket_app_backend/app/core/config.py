from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    jwt_secret: str = "20192104009.H4cH1"
    jwt_algorithm: str = "H256"
    jwt_expiration_minutes: int = 30

    class Config:
        env_file = ".env"

settings = Settings()