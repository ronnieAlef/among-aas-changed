from pydantic import BaseModel


class CreateDbRequest(BaseModel):
    # TODO: check the prefix of the db name ->
    db_name: str
    # TODO: check that the name has at least 3 chars
    username: str
