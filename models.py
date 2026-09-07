from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from database import Base

class Track(Base):
    __tablename__ = "tracks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    file_path = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class AcousticFingerprint(Base):
    __tablename__ = "fingerprints"

    id = Column(Integer, primary_key=True, index=True)
    track_id = Column(Integer, ForeignKey("tracks.id"))
    fingerprint_raw = Column(Text, nullable=False)
    duration = Column(Integer, nullable=False)

class DetectionLog(Base):
    __tablename__ = "detection_logs"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    status = Column(String, default="PENDING")
    results_json = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())