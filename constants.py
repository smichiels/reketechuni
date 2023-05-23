DIFFICULTY_LEVEL_DICT = {
    0: "BAS",
    1: "ADV",
    2: "EXP",
    3: "MAS",
    4: "ULT",
    5: "WORLD'S END",
}

GET_PROFILE_DATA = """SELECT user_name, level, player_rating, highest_rating  FROM chusan_user_data where id = 1;"""

GET_RECENT_SONGS = (
    """SELECT property_value FROM chusan_user_general_data WHERE user_id = 1;"""
)

GET_RECORDS = """ SELECT cmd.music_id, cm.name, cm.sort_name, cml.diff, cml.level, cml.level_decimal, cmd.score_max, cmd.is_all_justice, cmd.is_full_combo
FROM chusan_user_music_detail cmd LEFT OUTER JOIN chusan_music_level cml ON cml.music_id = cmd.music_id AND cml.diff = cmd.level 
LEFT OUTER JOIN chusan_music cm ON cmd.music_id = cm.music_id 
WHERE cml.enable = 1 
ORDER BY cmd.music_id ASC"""

DB_PATH = "<DB_PATH>"
