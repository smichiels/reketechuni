CREATE TABLE IF NOT EXISTS reketechuni_records (
    music_id INTEGER NOT NULL,
    name VARCHAR(255),
    sort_name VARCHAR(255),
    diff VARCHAR NOT NULL,
    level VARCHAR NOT NULL,
    score_max INTEGER NOT NULL,
    rank VARCHAR NOT NULL,
    constant FLOAT NOT NULL,
    rating FLOAT NOT NULL,
    is_all_justice BOOLEAN NOT NULL,
    is_full_combo BOOLEAN NOT NULL,
    PRIMARY KEY (music_id, score_max)
);
CREATE TABLE IF NOT EXISTS reketechuni_recent_10 (
    music_id INTEGER NOT NULL,
    name VARCHAR(255),
    sort_name VARCHAR(255),
    diff VARCHAR NOT NULL,
    level VARCHAR NOT NULL,
    score_max INTEGER NOT NULL,
    rank VARCHAR NOT NULL,
    constant FLOAT NOT NULL,
    rating FLOAT NOT NULL,
    is_all_justice BOOLEAN NOT NULL,
    is_full_combo BOOLEAN NOT NULL,
    PRIMARY KEY (music_id, score_max)
);
CREATE TABLE IF NOT EXISTS reketechuni_profile (
    user_name VARCHAR(255) NOT NULL,
    level INTEGER,
    ingame_rating FLOAT,
    calculated_rating FLOAT,
    max_rating FLOAT,
    avg_best_30 FLOAT,
    avg_rcnt_10 FLOAT,
    best_30_highest FLOAT,
    best_30_lowest FLOAT,
    PRIMARY KEY (user_name)
);
CREATE TABLE IF NOT EXISTS reketechuni_profile_historic (
    rating FLOAT NOT NULL,
    avg_best_30 FLOAT,
    avg_rcnt_10 FLOAT,
    date DATE NOT NULL,
    PRIMARY KEY (rating, date)
);
