from datetime import datetime, timezone
from typing import List, Optional

from fastapi import FastAPI, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

import database
import models
from logger import module_logger
from schemas import ContestsResp

module_logger("uvicorn.access")

models.init()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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


@app.get("/contests.json", response_model=List[ContestsResp])
def contests_json(
    include: Optional[List[str]] = Query([]),
    includes: Optional[List[str]] = Query([], alias="include[]"),
    exclude: Optional[List[str]] = Query([]),
    excludes: Optional[List[str]] = Query([], alias="exclude[]"),
    db: Session = Depends(database.get_db),
):
    include += includes
    exclude += excludes
    now = datetime.now(tz=timezone.utc)
    query = (
        db.query(models.Contest)
        .join(models.Platform, models.Platform.id == models.Contest.platform_id)
        .filter(models.Contest.end_time >= now)
    )
    if include:
        query = query.filter(models.Platform.source.in_(include))
    if exclude:
        query = query.filter(models.Platform.source.notin_(exclude))
    contests = query.order_by(models.Contest.start_time).all()
    resp = []
    for item in contests:
        item: models.Contest
        contest = ContestsResp(
            contest_id=item.contest_id,
            source=item.platform.source,
            name=item.name,
            link=item.link,
            start_time=item.start_time.isoformat(),
            end_time=item.end_time.isoformat(),
        )
        resp.append(contest)

    return resp
