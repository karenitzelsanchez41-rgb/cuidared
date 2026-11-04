from fastapi import FastAPI

from app.config import settings

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="API de la plataforma de vinculación de cuidados (prototipo académico).",
)


@app.get("/health", tags=["sistema"])
def health() -> dict[str, str]:
    """Comprueba que el servicio está arriba."""
    return {"status": "ok", "app": settings.app_name}
