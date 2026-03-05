import uuid
from typing import Annotated

from fastapi import APIRouter, Body

from src.riposetories.deployments import create_new_mongo_db
from src.requests.create_db_request import CreateDbRequest

router = APIRouter(
    tags=['deployments'],
    prefix='/deployments'
)


@router.post("")
async def create_new_db(create_db_request: Annotated[CreateDbRequest, Body()]):
    create_new_mongo_db(create_db_request)


@router.get("")
async def get_deployment_details(deployment_id: uuid):
    pass

