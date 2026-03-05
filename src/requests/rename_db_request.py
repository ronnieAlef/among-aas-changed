from pydantic import BaseModel


class RenameDbRequest(BaseModel):
    db_name: str
