from datetime import datetime, timezone

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

import database
import models
from logger import module_logger

module_logger("uvicorn.access")

models.init()

app = FastAPI()


@app.get("/")
def main(db: Session = Depends(database.get_db)):
    platforms = db.query(models.Platform).all()
    data = {
        "GitHub": "https://github.com/MeiK2333/recent_contests",
        "message": "The web api allows cross-domain access, you can reference this data directly, but please indicate "
        "the data source",
        "contests_link": f"https://contests.sdutacm.cn/contests.json",
        "updated_at": platforms,
    }
    return data


@app.get("/contests.json")
def contests_json(db: Session = Depends(database.get_db)):
    now = datetime.now(tz=timezone.utc)
    contests = (
        db.query(models.Contest)
        .filter(models.Contest.end_time >= now)
        .order_by(models.Contest.start_time)
        .all()
    )
    return contests
