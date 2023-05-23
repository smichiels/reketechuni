DIFFICULTY_LEVEL_DICT = {
    0: "BAS",
    1: "ADV",
    2: "EXP",
    3: "MAS",
    4: "ULT",
    5: "WORLD'S END",
}

SCORE_RANKS_LIST = [
    (500000, "D"),
    (600000, "C"),
    (700000, "B"),
    (800000, "BB"),
    (900000, "BBB"),
    (925000, "A"),
    (950000, "AA"),
    (975000, "AAA"),
    (990000, "S"),
    (1000000, "S+"),
    (1005000, "SS"),
    (1007500, "SS+"),
    (1009000, "SSS"),
]


SCORE_RATING_FORMULA_LIST = [
    (1009000, lambda constant, score: constant + 2.15),
    (1007500, lambda constant, score: constant + 2 + 0.15 * (score - 1007500) / 1500),
    (1005000, lambda constant, score: constant + 1.5 + 0.5 * (score - 1005000) / 2500),
    (1000000, lambda constant, score: constant + 1 + 0.5 * (score - 1000000) / 5000),
    (975000, lambda constant, score: constant + (score - 975000) / 25000),
    (925000, lambda constant, score: constant - 3 * (975000 - score) / 50000),
    (900000, lambda constant, score: constant - 3 - 2 * (925000 - score) / 25000),
    (800000, lambda constant, score: ((constant - 5) * (900000 - score) / 100000) * 0.5),
]


GET_PROFILE_DATA = """SELECT user_name, level, player_rating, highest_rating  FROM chusan_user_data where id = 1;"""

GET_RECENT_SONGS = """SELECT property_value FROM chusan_user_general_data WHERE user_id = 1;"""

GET_RECORDS = """ SELECT cmd.music_id, cm.name, cm.sort_name, cml.diff, cml.level, cml.level_decimal, cmd.score_max, cmd.is_all_justice, cmd.is_full_combo
FROM chusan_user_music_detail cmd LEFT OUTER JOIN chusan_music_level cml ON cml.music_id = cmd.music_id AND cml.diff = cmd.level 
LEFT OUTER JOIN chusan_music cm ON cmd.music_id = cm.music_id 
WHERE cml.enable = 1 
ORDER BY cmd.music_id ASC"""

DB_PATH = "<DB_PATH>"
