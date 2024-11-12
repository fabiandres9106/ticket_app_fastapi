from pydantic_settings import BaseSettings
from pydantic import EmailStr

class Settings(BaseSettings):
    database_url: str
    jwt_secret: str = "20192104009.H4cH1"
    jwt_algorithm: str = "H256"
    jwt_expiration_minutes: int = 30

    # Credenciales Email
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: EmailStr
    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_STARTTLS: bool = False  # Cambiado de MAIL_TLS a MAIL_STARTTLS
    MAIL_SSL_TLS: bool = True    # Cambiado de MAIL_SSL a MAIL_SSL_TLS

    debug: bool = False


    class Config:
        env_file = ".env"

settings = Settings()