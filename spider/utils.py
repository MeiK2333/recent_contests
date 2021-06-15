from datetime import datetime, timezone
from typing import List

from sqlalchemy.orm import Session

import models
import schemas
from database import SessionLocal
from logger import module_logger

logger = module_logger("spider")


def update_platform(platform_name: str, contests: List[schemas.Contest]):
    db: Session = SessionLocal()
    platform = (
        db.query(models.Platform)
        .filter(models.Platform.source == platform_name)
        .first()
    )
    for item in contests:
        contest = (
            db.query(models.Contest)
            .filter(models.Contest.contest_id == item.contest_id)
            .first()
        )
        if contest is None:
            contest = models.Contest()
        contest.platform = platform
        contest.contest_id = item.contest_id
        contest.link = item.link
        contest.name = item.name
        contest.start_time = item.start_time
        contest.end_time = item.end_time
        db.add(contest)
        logger.info(f"{platform_name} update {item.json(ensure_ascii=False)}")
    platform.updated_at = datetime.now(tz=timezone.utc)
    db.commit()
    db.close()
