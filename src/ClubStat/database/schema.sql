PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS user_roles (
    user_role_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS reservation_status (
    reservation_status_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS coach (
    coach_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    surname TEXT NOT NULL,
    patronymic TEXT
);
CREATE TABLE IF NOT EXISTS workout (
    workout_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    surname TEXT NOT NULL,
    patronymic TEXT,
    login TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    user_role INTEGER NOT NULL REFERENCES user_roles(user_role_id)
);
CREATE TABLE IF NOT EXISTS coach_workout (
    coach_workout_id INTEGER PRIMARY KEY AUTOINCREMENT,
    coach_id INTEGER NOT NULL REFERENCES coach(coach_id) ON DELETE CASCADE,
    workout_id INTEGER NOT NULL REFERENCES workout(workout_id) ON DELETE CASCADE,
    UNIQUE(coach_id, workout_id)
);
CREATE TABLE IF NOT EXISTS reservation (
    reservation_id INTEGER PRIMARY KEY AUTOINCREMENT,
    admin_id INTEGER REFERENCES users(user_id),
    visitor_id INTEGER NOT NULL REFERENCES users(user_id),
    workout_id INTEGER NOT NULL REFERENCES workout(workout_id),
    reservation_date TEXT NOT NULL,
    status INTEGER NOT NULL REFERENCES reservation_status(reservation_status_id)
);
CREATE INDEX IF NOT EXISTS idx_reservation_visitor ON reservation(visitor_id);
CREATE INDEX IF NOT EXISTS idx_reservation_workout ON reservation(workout_id);
INSERT OR IGNORE INTO user_roles(user_role_id, name) VALUES (1, 'admin'), (2, 'visitor');
INSERT OR IGNORE INTO reservation_status(reservation_status_id, name) VALUES (1, 'active'), (2, 'cancelled');
