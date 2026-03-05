from typing import Annotated

from fastapi import APIRouter, Body
from starlette import status
from starlette.responses import JSONResponse

from src.models.deployment import Deployment
from src.repositories.deployments import create_new_mongo_db, return_deployment_details
from src.requests.create_db_request import CreateDbRequest

router = APIRouter(
    tags=['deployments'],
    prefix='/deployments'
)


@router.post("")
async def create_new_db(create_db_request: Annotated[CreateDbRequest, Body()]):
    try:
        create_new_mongo_db(create_db_request)
        return JSONResponse(content="created db", status_code=status.HTTP_200_OK)
    except:
        return JSONResponse(content="error", status_code=status.HTTP_400_BAD_REQUEST)


@router.get("", response_model=Deployment)
async def get_deployment_details(deployment_id: str):

    data = return_deployment_details(deployment_id)
    return data

