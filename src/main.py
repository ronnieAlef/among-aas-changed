import uvicorn
from fastapi import FastAPI
from routers import deployments_router
from src.postgres_client import connect_to_postgres

app = FastAPI()
app.include_router(deployments_router)


if __name__ == "__main__":
    connect_to_postgres()
    uvicorn.run(app, host="127.0.0.1", port=8080)

