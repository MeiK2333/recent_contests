from datetime import datetime, timezone
from typing import List

from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship, Session
from sqlalchemy.types import TypeDecorator

from config import platforms
from database import Base, engine, SessionLocal
from logger import module_logger

logger = module_logger("models")


class TZDateTime(TypeDecorator):
    impl = TIMESTAMP()
    cache_ok = True

    def process_bind_param(self, value: datetime, dialect):
        # 传入的参数必须有 tz info 信息
        if isinstance(value, datetime) and value.tzinfo is None:
            raise ValueError("{!r} must be TZ-aware".format(value))
        # 转换为 utc 时间存储
        date = value.astimezone(tz=timezone.utc)
        return date

    def process_result_value(self, value: datetime, dialect):
        # 返回的数据都是 utc+0 保存的，以 iso 格式将其转换为 utc 时间
        # 精度为 S 即可，因为对于我们的需求，更高的精度也没有意义
        iso = value.strftime("%Y-%m-%dT%H:%M:%S+00:00")
        date = datetime.fromisoformat(iso)
        return date


class Platform(Base):
    __tablename__ = "platforms"

    id = Column(Integer, primary_key=True, index=True)
    source = Column(String(256), unique=True)
    link = Column(String(256))
    updated_at = Column(
        TZDateTime, default=datetime(1970, 1, 1, 0, 0, 0, 0, tzinfo=timezone.utc)
    )

    contests: List['Contest']
    contests = relationship("Contest", back_populates="platform")


class Contest(Base):
    __tablename__ = "contests"

    id = Column(Integer, primary_key=True, index=True)
    contest_id = Column(String(256), unique=True)
    name = Column(String(256))
    link = Column(String(256))
    start_time: datetime
    start_time = Column(TZDateTime)
    end_time: datetime
    end_time = Column(TZDateTime)

    platform_id = Column(Integer, ForeignKey("platforms.id"))
    platform: Platform
    platform = relationship("Platform", back_populates="contests")


def init():
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()

    for item in platforms:
        platform = db.query(Platform).filter(Platform.source == item["source"]).first()
        if platform is None:
            platform = Platform(source=item["source"], link=item["link"])
            db.add(platform)
            db.commit()
            logger.info(f"insert platform {platform.source} {platform.link}")

    db.close()


init()
