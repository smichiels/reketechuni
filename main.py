import logging.config

import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

from constants import (
    GET_PROFILE_DATA,
    GET_RECENT_SONGS,
    GET_RECORDS,
    DB_PATH,
)
from loader import load_data
from transformer import (
    transform_into_reketechuni_records,
    transform_into_reketechuni_profile,
    transform_into_reketechuni_recent_10,
)
from utils import check_if_tables_exist

logging.config.fileConfig("logging.ini")
logger = logging.getLogger("root")


def get_chusan_records(db_engine):
    return pd.read_sql(GET_RECORDS, db_engine)


def get_chusan_best_recent_10(db_session):
    values = [x[0] for x in db_session.execute(text(GET_RECENT_SONGS))][0]
    real_values = [x.split(":") for x in values.split(",")]
    df = pd.DataFrame(real_values, columns=["music_id", "level", "score_max"])
    return df


def get_chusan_profile(db_session):
    values = [x for x in db_session.execute(text(GET_PROFILE_DATA))][0]
    values_dict = {
        "user_name": [values[0]],
        "level": [values[1]],
        "ingame_rating": [values[2] / 100],
        "max_rating": [values[3] / 100],
    }
    return values_dict


if __name__ == "__main__":
    engine = create_engine(f"sqlite:///{DB_PATH}")
    with Session(engine) as session:
        # check if any reketechuni tables do not exist
        check_if_tables_exist(engine, session)

        # get data
        logging.info("Getting chusan data...")
        df_chusan_records = get_chusan_records(engine)
        df_chusan_recent_10 = get_chusan_best_recent_10(session)
        chusan_profile = get_chusan_profile(session)

        # transform data
        logging.info("Transforming chusan data into reketechuni format...")
        df_reketechuni_records = transform_into_reketechuni_records(df_chusan_records)
        df_reketechuni_recent_10 = transform_into_reketechuni_recent_10(
            df_chusan_recent_10, df_reketechuni_records
        )
        (
            df_reketechuni_profile,
            profile_historic_entry,
        ) = transform_into_reketechuni_profile(
            chusan_profile, df_reketechuni_records, df_reketechuni_recent_10
        )

        # load data
        logging.info("Saving reketechuni info into database...")
        load_data(
            session,
            engine,
            df_reketechuni_records,
            df_reketechuni_recent_10,
            df_reketechuni_profile,
            profile_historic_entry,
        )
        logging.info("Done!! \o/")