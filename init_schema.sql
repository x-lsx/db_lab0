DROP TABLE IF EXISTS game_platforms CASCADE;
DROP TABLE IF EXISTS game_developers CASCADE;
DROP TABLE IF EXISTS game_ceremonies CASCADE;
DROP TABLE IF EXISTS game_languages CASCADE;
DROP TABLE IF EXISTS modes_in_game CASCADE;
DROP TABLE IF EXISTS platforms CASCADE;
DROP TABLE IF EXISTS main_developers CASCADE;
DROP TABLE IF EXISTS ceremonies CASCADE;
DROP TABLE IF EXISTS languages CASCADE;
DROP TABLE IF EXISTS games CASCADE;
DROP TABLE IF EXISTS genres CASCADE;
DROP TABLE IF EXISTS companies CASCADE;
DROP TABLE IF EXISTS countries CASCADE;
DROP TABLE IF EXISTS game_modes CASCADE;

-- Создание таблицы стран
CREATE TABLE countries (
    country_id SERIAL PRIMARY KEY,
    country_name VARCHAR(100) NOT NULL
);

-- Создание таблицы компаний
CREATE TABLE companies (
    company_id SERIAL PRIMARY KEY,
    company_name VARCHAR(255) NOT NULL,
    company_foundation INTEGER,
    country_id INTEGER REFERENCES countries(country_id)
);

-- Создание таблицы жанров
CREATE TABLE genres (
    genre_id SERIAL PRIMARY KEY,
    genre_name VARCHAR(100) NOT NULL,
    genre_description TEXT
);

-- Создание таблицы игр
CREATE TABLE games (
    game_id SERIAL PRIMARY KEY,
    game_name VARCHAR(255) NOT NULL,
    release_date DATE,
    rating DECIMAL(3,1),
    genre_id INTEGER REFERENCES genres(genre_id),
    company_id INTEGER REFERENCES companies(company_id)
);

-- Создание таблицы платформ
CREATE TABLE platforms (
    platform_id SERIAL PRIMARY KEY,
    platform_name VARCHAR(100) NOT NULL,
    platform_description TEXT
);

-- Создание связующей таблицы игр и платформ
CREATE TABLE game_platforms (
    platform_id INTEGER REFERENCES platforms(platform_id),
    game_id INTEGER REFERENCES games(game_id),
    PRIMARY KEY (platform_id, game_id)
);

-- Создание таблицы разработчиков
CREATE TABLE main_developers (
    main_developers_id SERIAL PRIMARY KEY,
    main_developers_name VARCHAR(100) NOT NULL,
    main_developers_surname VARCHAR(100) NOT NULL,
    main_developers_date_birth DATE
);

-- Создание связующей таблицы игр и разработчиков
CREATE TABLE game_developers (
    main_developers_id INTEGER REFERENCES main_developers(main_developers_id),
    game_id INTEGER REFERENCES games(game_id),
    PRIMARY KEY (main_developers_id, game_id)
);

-- Создание таблицы церемоний
CREATE TABLE ceremonies (
    ceremony_id SERIAL PRIMARY KEY,
    ceremony_name VARCHAR(255) NOT NULL,
    ceremony_foundation INTEGER
);

-- Создание связующей таблицы игр и церемоний
CREATE TABLE game_ceremonies (
    ceremony_id INTEGER REFERENCES ceremonies(ceremony_id),
    game_id INTEGER REFERENCES games(game_id),
    ceremony_year INTEGER,
    PRIMARY KEY (ceremony_id, game_id)
);

-- Создание таблицы языков
CREATE TABLE languages (
    language_interface_id SERIAL PRIMARY KEY,
    language_interface_name VARCHAR(100) NOT NULL
);

-- Создание связующей таблицы игр и языков
CREATE TABLE game_languages (
    language_interface_id INTEGER REFERENCES languages(language_interface_id),
    game_id INTEGER REFERENCES games(game_id),
    PRIMARY KEY (language_interface_id, game_id)
);

-- Создание таблицы режимов игры
CREATE TABLE game_modes (
    game_mode_id SERIAL PRIMARY KEY,
    game_mode_name VARCHAR(100) NOT NULL
);

-- Создание связующей таблицы игр и режимов игры
CREATE TABLE modes_in_game(
    game_mode_id INTEGER REFERENCES game_modes(game_mode_id),
    game_id INTEGER REFERENCES games(game_id),
    PRIMARY KEY (game_mode_id, game_id)
);