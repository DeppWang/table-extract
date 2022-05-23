DROP TABLE IF EXISTS comments;
DROP TABLE IF EXISTS user;

CREATE TABLE comments
(
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    content      VARCHAR   NOT NULL,
    parent       INTEGER            DEFAULT 0,
    username     VARCHAR,
    created_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);



CREATE TABLE user
(
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    email    VARCHAR UNIQUE NOT NULL,
    username VARCHAR UNIQUE NOT NULL,
    password VARCHAR        NOT NULL
);