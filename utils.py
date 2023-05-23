import logging

from sqlalchemy import delete, inspect, text

from models import (
    ReketechuniRecords,
    ReketechuniRecent10,
    ReketechuniProfile,
    ReketechuniProfileHistoric,
)

logger = logging.getLogger("root")


def get_rank_str(rating):
    if rating < 500000:
        return "D"
    elif rating < 600000:
        return "C"
    elif rating < 700000:
        return "B"
    elif rating < 800000:
        return "BB"
    elif rating < 900000:
        return "BBB"
    elif rating < 925000:
        return "A"
    elif rating < 950000:
        return "AA"
    elif rating < 975000:
        return "AAA"
    elif rating < 990000:
        return "S"
    elif rating < 1000000:
        return "S+"
    elif rating < 1005000:
        return "SS"
    elif rating < 1007500:
        return "SS+"
    elif rating < 1009000:
        return "SSS"
    else:
        return "SSS+"


def get_level_str(level_decimal):
    [i, d] = str(level_decimal).split(".")
    if int(d) >= 5:
        return i + "+"
    return i


def calculate_rating(score, constant):
    if score >= 1009000:
        rating = constant + 2.15
    elif score >= 1007500:
        rating = constant + 2 + 0.15 * (score - 1007500) / 1500
    elif score >= 1005000:
        rating = constant + 1.5 + 0.5 * (score - 1005000) / 2500
    elif score >= 1000000:
        rating = constant + 1 + 0.5 * (score - 1000000) / 5000
    elif score >= 975000:
        rating = constant + 1 * (score - 975000) / 25000
    elif score >= 925000:
        rating = constant - 3 * (975000 - score) / 50000
    elif score >= 900000:
        rating = constant - 3 - 2 * (925000 - score) / 25000
    elif score >= 800000:
        rating = ((constant - 5) * (900000 - score) / 100000) * 0.5
    else:
        rating = 0
    return round(rating, 2)


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
            logger.warning(
                f"Table {table} was not found in db!! Checking and creating all missing tables... "
            )
            with open("create_tables.sql", "r") as f:
                for stmt in f.read().split(";"):
                    session.execute(text(stmt))
            return
    logger.info("All tables are OK!! Let's continue")
