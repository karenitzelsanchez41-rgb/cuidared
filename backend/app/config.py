from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuración leída de variables de entorno (o del archivo .env)."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "CuidaRed API"
    database_url: str = "sqlite:///./cuidared.db"
    secret_key: str = "solo-para-desarrollo"
    access_token_expire_minutes: int = 60
    # Claves AGEB prioritarias (del Observatorio), separadas por comas.
    agebs_prioritarias: str = ""

    @property
    def agebs_prioritarias_lista(self) -> set[str]:
        return {x.strip() for x in self.agebs_prioritarias.split(",") if x.strip()}


settings = Settings()
