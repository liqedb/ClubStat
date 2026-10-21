DROP TABLE IF EXISTS reservation;
DROP TABLE IF EXISTS coach_workout;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS workout;  
DROP TABLE IF EXISTS coach; 
DROP TABLE IF EXISTS reservation_status;
DROP TABLE IF EXISTS user_roles;

CREATE TABLE user_roles(
    user_role_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE reservation_status(
    reservation_status_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE coach(
    coach_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    surname TEXT NOT NULL,
    patronymic TEXT
);

CREATE TABLE workout(
    workout_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT NOT NULL UNIQUE
);

CREATE TABLE users(
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    surname TEXT NOT NULL,
    patronymic TEXT,
    login TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    user_role INTEGER NOT NULL,
    FOREIGN KEY (user_role) REFERENCES user_roles (user_role_id)
);


CREATE TABLE coach_workout(
    coach_workout_id INTEGER PRIMARY KEY AUTOINCREMENT,
    coach_id INTEGER NOT NULL,
    workout_id INTEGER NOT NULL,
    FOREIGN KEY (coach_id) REFERENCES coach (coach_id),
    FOREIGN KEY (workout_id) REFERENCES workout (workout_id)
);



CREATE TABLE reservation(
    reservation_id INTEGER PRIMARY KEY AUTOINCREMENT,
    admin_id INTEGER,
    visitor_id INTEGER NOT NULL,
    workout_id INTEGER NOT NULL,
    reservation_date TEXT NOT NULL,
    status INTEGER NOT NULL,
    FOREIGN KEY (admin_id) REFERENCES users (user_id),
    FOREIGN KEY (visitor_id) REFERENCES users (user_id),
    FOREIGN KEY (workout_id) REFERENCES workout (workout_id),
    FOREIGN KEY (status) REFERENCES reservation_status (reservation_status_id)
);


INSERT INTO user_roles (name) VALUES 
    ('admin'),
    ('visitor');

INSERT INTO coach (name, surname, patronymic) VALUES 
    ('Иван', 'Петров', 'Сергеевич'),
    ('Мария', 'Сидорова', NULL);

INSERT INTO workout (name, description) VALUES 
    ('Йога', 'Занятие по йоге для начинающих'),
    ('Кроссфит', 'Высокоинтенсивная функциональная тренировка');


INSERT INTO users (name, surname, patronymic, login, password, user_role) VALUES 
    ('Админ', 'Системы', NULL, 'admin', 'admin123', 1),
    ('Михаил', 'Петров', 'Сергеевич', 'misha2008', 'legend', 2);

INSERT INTO coach_workout (coach_id, workout_id) VALUES 
    (1, 1)
    (2, 2);

INSERT INTO reservation (admin_id, visitor_id, workout_id, reservation_date, status) VALUES 
    (1, 1, 1, '2026-10-8 10:00', 2), 
    (1, 2, 2, '2026-10-9 18:00', 1);
