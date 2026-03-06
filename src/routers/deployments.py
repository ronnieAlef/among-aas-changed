from typing import Annotated

from fastapi import APIRouter, Body, Header
from starlette import status

from src.models.headers.delete_db_header import DeleteDbHeader
from src.models.deployment import Deployment
from src.repositories.deployments import create_new_mongo_db, return_deployment_details, change_db_name, delete_mongo_db
from src.models.requests.create_db_request import CreateDbRequest
from src.models.requests.rename_db_request import RenameDbRequest

router = APIRouter(
    tags=['deployments'],
    prefix='/deployments'
)


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_new_db(create_db_request: Annotated[CreateDbRequest, Body()]):
    generated_id = create_new_mongo_db(create_db_request)
    json_text = {"id": generated_id}
    return json_text


@router.get("", response_model=Deployment, status_code=status.HTTP_200_OK)
async def get_deployment_details(deployment_id: str):
    data = return_deployment_details(deployment_id)
    return data


@router.put("/", status_code=status.HTTP_200_OK)
async def update_db_name(new_db_name: Annotated[RenameDbRequest, Body()], deployment_id: str):
    generated_id = change_db_name(new_db_name, deployment_id)
    json_text = {"id": generated_id}
    return "sorry:("


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
async def delete_db(deployment_id: str, delete_db_header: Annotated[DeleteDbHeader, Header()]):
    generated_id = delete_mongo_db(deployment_id, delete_db_header)
    json_text = {"id": generated_id}
    return json_text


@router.get("/connection_string")
async def get_connection_string():
    pass

