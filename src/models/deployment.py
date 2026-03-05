import uuid
from datetime import datetime
from typing import Literal

from pydantic import BaseModel


class Deployment(BaseModel):
    id: uuid.UUID
    db_name: str
    status: Literal["DELETED", "CREATED"]
    username: str
    creation_time: datetime
