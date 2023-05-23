import logging
from datetime import date

from models import (
    ReketechuniRecent10,
    ReketechuniProfile,
    ReketechuniProfileHistoric,
    ReketechuniRecords,
)
from utils import wipe_tables

logger = logging.getLogger("root")


def load_data(
    session, engine, df_records, df_recent_10, df_profile, profile_historic_entry
):
    wipe_tables(session)
    df_records.to_sql(
        ReketechuniRecords.__tablename__, engine, if_exists="append", index=False
    )
    df_recent_10.to_sql(
        ReketechuniRecent10.__tablename__, engine, if_exists="append", index=False
    )
    df_profile.to_sql(
        ReketechuniProfile.__tablename__, engine, if_exists="append", index=False
    )
    row = session.query(ReketechuniProfileHistoric).filter_by(date=date.today()).first()
    if row is None:
        logger.info("No profile history entry for today. Creating...")
        obj = ReketechuniProfileHistoric(**profile_historic_entry)
        session.add(obj)
    else:
        logger.info("Found existing profile history entry for today. Updating...")
        row.rating = profile_historic_entry["rating"]
        row.avg_best_30 = profile_historic_entry["avg_best_30"]
        row.avg_rcnt_10 = profile_historic_entry["avg_rcnt_10"]
    session.commit()
