/* delete if table already exists */
DROP TABLE IF EXISTS user;

/* creates a user table with primary key id */
CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    first_name TEXT NOT NULL,
    last_name  TEXT NOT NULL
);