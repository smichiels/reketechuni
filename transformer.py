from datetime import date

import pandas as pd

from constants import DIFFICULTY_LEVEL_DICT, REKETECHUNI_RECORDS_COLUMNS
from utils import get_rank_str, get_level_str, calculate_rating, get_score_to_reach_rating


def transform_into_reketechuni_records(df, df_existing_records):
    df["diff"] = df["diff"].apply(DIFFICULTY_LEVEL_DICT.get)
    df["rank"] = df["score_max"].apply(get_rank_str)
    df["constant"] = (df["level"].astype(str) + "." + df["level_decimal"].astype(str)).astype(float)
    df["level"] = df["constant"].apply(get_level_str)
    df["rating"] = df[["constant", "score_max"]].apply(lambda x: calculate_rating(*x), axis=1)
    df.drop(df[df["diff"] == "WORLD'S END"].index, inplace=True)
    df.drop(columns=["level_decimal"], inplace=True)
    updated_songs_indexes = set(
        pd.concat([df[REKETECHUNI_RECORDS_COLUMNS], df_existing_records[REKETECHUNI_RECORDS_COLUMNS]])
        .drop_duplicates(keep=False)
        .index
    )
    df = pd.merge(df, df_existing_records, how="left", on=["music_id", "diff"])
    df.loc[df.index.isin(updated_songs_indexes), "updated"] = date.today()
    df["updated"] = [x.date() for x in pd.to_datetime(df["updated"])]
    return df


def transform_into_reketechuni_recent_10(df, df_reketechuni_records):
    df["diff"] = df["level"].astype(int).apply(DIFFICULTY_LEVEL_DICT.get)
    df["music_id"] = df["music_id"].astype(int)
    df.drop(columns=["level"], inplace=True)
    df = pd.merge(
        df,
        df_reketechuni_records[["music_id", "diff", "name", "sort_name", "level", "constant"]],
        how="left",
        left_on=["music_id", "diff"],
        right_on=["music_id", "diff"],
    )
    df["score_max"] = df["score_max"].astype(int)
    df["rank"] = df["score_max"].apply(get_rank_str)
    df["rating"] = df[["constant", "score_max"]].apply(lambda x: calculate_rating(*x), axis=1)
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
        "rating": values["ingame_rating"][0],
        "avg_best_30": values["avg_best_30"][0],
        "avg_rcnt_10": values["avg_rcnt_10"][0],
        "date": date.today(),
    }
    return df_profile, profile_historic_entry


def calculate_recomendations(df_reketechuni_records):
    df_reketechuni_records = df_reketechuni_records.drop(columns=["updated"]).sort_values(by="rating", ascending=False)
    rating_to_reach = df_reketechuni_records.iloc[:30, :].tail(1)["rating"].values[0] + 0.01
    df_candidates = df_reketechuni_records.iloc[30:, :].copy()
    df_candidates["max_achievable_rating"] = df_candidates["constant"].apply(lambda x: calculate_rating(x, 1010000))
    df_candidates.drop(df_candidates[df_candidates["max_achievable_rating"] < rating_to_reach].index, inplace=True)
    df_candidates["score_to_reach"] = df_candidates["constant"].apply(
        lambda constant: get_score_to_reach_rating(rating_to_reach, constant)
    )
    df_candidates["score_delta"] = df_candidates.apply(lambda x: x["score_to_reach"] - x["score_max"], axis=1)
    df_candidates.drop(columns=["max_achievable_rating", "is_full_combo", "is_all_justice"], inplace=True)
    return df_candidates.sort_values(by="score_delta").head(20)
