import uvicorn
from fastapi import FastAPI
from routers import deployments_router

app = FastAPI()
app.include_router(deployments_router)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=80)

