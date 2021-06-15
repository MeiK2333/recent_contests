import hashlib
from datetime import datetime

from pydantic import BaseModel, validator


class Platform(BaseModel):
    name: str
    link: str

    class Config:
        orm_mode = True


class Contest(BaseModel):
    contest_id: str
    name: str
    link: str
    start_time: datetime
    end_time: datetime

    class Config:
        orm_mode = True


class ContestsResp(BaseModel):
    source: str
    name: str
    link: str
    contest_id: str
    start_time: str
    end_time: str
    hash: str = ""

    @validator("hash", always=True)
    def populate_hash(cls, v, values) -> str:
        hash_str = (
            values['source']
            + values['name']
            + values['link']
            + values['start_time']
            + values['end_time']
        )
        s = hashlib.sha1()
        s.update(hash_str.encode())
        return s.hexdigest()

    class Config:
        orm_mode = True
