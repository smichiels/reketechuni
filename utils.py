import logging

from sqlalchemy import delete, inspect, text

from constants import SCORE_RANKS_LIST, SCORE_RATING_FORMULA_LIST
from models import (
    ReketechuniRecords,
    ReketechuniRecent10,
    ReketechuniProfile,
    ReketechuniProfileHistoric,
)

logger = logging.getLogger("root")


def get_rank_str(rating):
    for score, rank in SCORE_RANKS_LIST:
        if rating < score:
            return rank
    return "SSS+"


def get_level_str(level_decimal):
    [i, d] = str(level_decimal).split(".")
    if int(d) >= 5:
        return i + "+"
    return i


def calculate_rating(constant, score_max):
    for score, formula, _ in SCORE_RATING_FORMULA_LIST:
        if score_max >= score:
            rating = formula(constant, score_max)
            return round(rating, 2)
    return 0


def get_score_to_reach_rating(rating_to_reach, constant):
    for s, f1, f2 in SCORE_RATING_FORMULA_LIST[1:]:
        s = s - 1
        if f1(constant, s) <= rating_to_reach:
            return int(f2(constant, rating_to_reach))
    return 1009000


def wipe_tables(session):
    session.execute(delete(ReketechuniRecords))
    session.execute(delete(ReketechuniRecent10))
    session.execute(delete(ReketechuniProfile))
    session.commit()


def check_if_tables_exist(engine, session):
    for table in [
        ReketechuniRecords,
        ReketechuniRecent10,
        ReketechuniProfile,
        ReketechuniProfileHistoric,
    ]:
        if not inspect(engine).has_table(table.__tablename__):
            logger.warning(f"Table {table} was not found in db!! Checking and creating all missing tables... ")
            with open("create_tables.sql", "r") as f:
                for stmt in f.read().split(";"):
                    session.execute(text(stmt))
            return
    logger.info("All tables are OK!! Let's continue")
