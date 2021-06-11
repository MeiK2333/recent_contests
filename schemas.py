from datetime import datetime

from pydantic import BaseModel


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
