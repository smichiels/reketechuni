from datetime import date

import pandas as pd

from constants import DIFFICULTY_LEVEL_DICT
from utils import get_rank_str, get_level_str, calculate_rating


def transform_into_reketechuni_records(df):
    df["diff"] = df["diff"].apply(DIFFICULTY_LEVEL_DICT.get)
    df["rank"] = df["score_max"].apply(get_rank_str)
    df["constant"] = (df["level"].astype(str) + "." + df["level_decimal"].astype(str)).astype(float)
    df["level"] = df["constant"].apply(get_level_str)
    df["rating"] = df[["score_max", "constant"]].apply(lambda x: calculate_rating(*x), axis=1)
    df.drop(df[df["diff"] == "WORLD'S END"].index, inplace=True)
    df.drop(columns=["level_decimal"], inplace=True)
    return df


def transform_into_reketechuni_recent_10(df, df_reketechuni_records):
    df["diff"] = df["level"].astype(int).apply(DIFFICULTY_LEVEL_DICT.get)
    df["music_id"] = df["music_id"].astype(int)
    df.drop(columns=["level"], inplace=True)
    df = pd.merge(
        df,
        df_reketechuni_records.drop(columns=["score_max"]),
        how="left",
        left_on=["music_id", "diff"],
        right_on=["music_id", "diff"],
    )
    df["score_max"] = df["score_max"].astype(int)
    return df.sort_values(by="rating", ascending=False).head(10)


def transform_into_reketechuni_profile(values, df_reketechuni_records, df_reketechuni_recent_10):
    df_records = df_reketechuni_records.sort_values(by="rating", ascending=False).head(30)
    best_30_sum = df_records["rating"].sum()
    best_recent_10_sum = df_reketechuni_recent_10["rating"].sum()
    values["calculated_rating"] = [round((best_recent_10_sum + best_30_sum) / 40, 2)]
    values["avg_best_30"] = [round(best_30_sum / 30, 2)]
    values["avg_rcnt_10"] = [round(best_recent_10_sum / 10, 2)]
    values["best_30_highest"] = df_records.head(1)["rating"].values
    values["best_30_lowest"] = df_records.tail(1)["rating"].values
    df_profile = pd.DataFrame(values)
    profile_historic_entry = {
        "rating": values["calculated_rating"][0],
        "avg_best_30": values["avg_best_30"][0],
        "avg_rcnt_10": values["avg_rcnt_10"][0],
        "date": date.today(),
    }
    return df_profile, profile_historic_entry
