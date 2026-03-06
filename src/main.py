import uvicorn
from fastapi import FastAPI

from routers import deployments_router
from src.exception_handlers import register_exception_handlers
from src.postgres_client import connect_to_postgres

app = FastAPI()
app.include_router(deployments_router)
register_exception_handlers(app)


if __name__ == "__main__":

    connect_to_postgres()
    uvicorn.run(app, host="127.0.0.1", port=8080)


