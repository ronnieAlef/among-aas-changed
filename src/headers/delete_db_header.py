from pydantic import BaseModel


class DeleteDbHeader(BaseModel):
    username: str
