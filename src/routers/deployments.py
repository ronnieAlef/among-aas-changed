from fastapi import APIRouter

router = APIRouter(
    tags=['deployments'],
    prefix='/deployments'
)


@router.post("")
async def testing_docs():
    return "thank you"
