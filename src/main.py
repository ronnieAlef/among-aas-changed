import uvicorn
from fastapi import FastAPI, Request
from starlette.responses import JSONResponse

from routers import deployments_router
from src.Errors import AmongAasException
from src.postgres_client import connect_to_postgres

app = FastAPI()
app.include_router(deployments_router)


# def register_exception_handlers(app):
#     @app.exception_handler(AmongAasException)
#     async def unicorn_exception_handler(request: Request, exc: AmongAasException):
#         return JSONResponse(
#             status_code=exc.status_code,
#             content={"error": exc.error_code,
#                      "message": exc.message},
#         )



if __name__ == "__main__":

    connect_to_postgres()
    uvicorn.run(app, host="127.0.0.1", port=8080)


