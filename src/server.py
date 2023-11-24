from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.config.database import create_db_and_tables

from src.routes.provas_routes import provas_router
from src.routes.provas_routes import provas_router
from src.routes.resultados_routes import resultados_provas_router
from src.routes.resultados_routes import provas_aplicadas_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(provas_router)
app.include_router(resultados_provas_router)
app.include_router(provas_aplicadas_router)


@app.get("/healthcheck")
def healthcheck():
    return {"status": "ok"}