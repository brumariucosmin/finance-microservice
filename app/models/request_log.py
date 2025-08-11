from sqlalchemy import Column, Integer, String, DateTime, JSON

from app.core.database import Base

import datetime


class RequestLog(Base):
    __tablename__ = "request_logs"
    id = Column(Integer, primary_key=True, index=True)
    operation = Column(String, index=True)
    params = Column(JSON)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
