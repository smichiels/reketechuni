from sqlalchemy import (
    Column,
    Integer,
    Float,
    String,
    Boolean,
    Date,
    PrimaryKeyConstraint,
)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class ReketechuniRecords(Base):
    __tablename__ = "reketechuni_records"

    music_id = Column(Integer, primary_key=True)
    name = Column(String(255))
    sort_name = Column(String(255))
    diff = Column(String, nullable=False)
    level = Column(String, nullable=False)
    score_max = Column(Integer, primary_key=True)
    rank = Column(String, nullable=False)
    constant = Column(Float, nullable=False)
    rating = Column(Float, nullable=False)
    is_all_justice = Column(Boolean, nullable=False)
    is_full_combo = Column(Boolean, nullable=False)

    __table_args__ = (PrimaryKeyConstraint("music_id", "score_max"),)


class ReketechuniRecent10(Base):
    __tablename__ = "reketechuni_recent_10"

    music_id = Column(Integer, primary_key=True)
    name = Column(String(255))
    sort_name = Column(String(255))
    diff = Column(String, nullable=False)
    level = Column(String, nullable=False)
    score_max = Column(Integer, primary_key=True)
    rank = Column(String, nullable=False)
    constant = Column(Float, nullable=False)
    rating = Column(Float, nullable=False)
    is_all_justice = Column(Boolean, nullable=False)
    is_full_combo = Column(Boolean, nullable=False)

    __table_args__ = (PrimaryKeyConstraint("music_id", "score_max"),)


class ReketechuniProfile(Base):
    __tablename__ = "reketechuni_profile"

    user_name = Column(String(255), primary_key=True)
    level = Column(Integer)
    ingame_rating = Column(Float)
    calculated_rating = Column(Float)
    max_rating = Column(Float)
    avg_best_30 = Column(Float)
    avg_rcnt_10 = Column(Float)
    best_30_highest = Column(Float)
    best_30_lowest = Column(Float)


class ReketechuniProfileHistoric(Base):
    __tablename__ = "reketechuni_profile_historic"

    rating = Column(Float, primary_key=True)
    avg_best_30 = Column(Float)
    avg_rcnt_10 = Column(Float)
    date = Column(Date, primary_key=True)

    __table_args__ = (PrimaryKeyConstraint("rating", "date"),)
