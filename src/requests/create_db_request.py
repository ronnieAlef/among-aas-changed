from typing import Annotated
import re

from pydantic import BaseModel, AfterValidator


def validate_db_name(db_name: str):
    pattern = re.compile("^user[0-9][0-9]")

    if not pattern.match(db_name):
        raise ValueError('DB name should start with a prefix of "userxx".')

    return db_name


def validate_username(username: str):
    if len(username) < 3:
        raise ValueError('The username should be at least 3 chars long.')
    return username


class CreateDbRequest(BaseModel):
    db_name: Annotated[str, AfterValidator(validate_db_name)]
    username: Annotated[str, AfterValidator(validate_username)]
