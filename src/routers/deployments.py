from fastapi import APIRouter

router = APIRouter(
    tags=['deployments'],
    prefix='/deployments'
)

@router.get("/testing/")
async def testing_docs():
    return "thank you"
