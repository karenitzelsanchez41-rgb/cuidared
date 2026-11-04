from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuración leída de variables de entorno (o del archivo .env)."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "CuidaRed API"
    database_url: str = "sqlite:///./cuidared.db"
    secret_key: str = "solo-para-desarrollo"


settings = Settings()
