"""
sql.py -- sql commands
======================
Used is database.py
"""

CREATE_USERS = """CREATE TABLE IF NOT EXISTS users(
                   username VARCHAR PRIMARY KEY,
                   password VARCHAR NOT NULL)"""

CREATE_SESSIONS = """CREATE TABLE IF NOT EXISTS sessions(
                      uuid VARCHAR PRIMARY KEY,
                      users VARCHAR NOT NULL,
                      players INT NOT NULL,
                      payload VARCHAR NOT NULL,
                      state VARCHAR NOT NULL,
                      round INT NOT NULL,
                      ts INT NOT NULL)"""

CREATE_ROUNDS = """CREATE TABLE IF NOT EXISTS rounds(
                    uuid VARCHAR,
                    round INT,
                    user_moves VARCHAR NOT NULL,
                    PRIMARY KEY(uuid, round))"""

SELECT_USER = "SELECT * FROM users WHERE username=?"
INSERT_USER = "INSERT INTO users VALUES (?, ?)"
SELECT_SESSION = "SELECT * FROM sessions WHERE uuid=?"
INSERT_SESSION = "INSERT INTO sessions VALUES (?,?,?,?,?,?,?)"
UPDATE_SESSION = """UPDATE sessions SET
                     users=?,
                     players=?,
                     payload=?,
                     state=?,
                     round=?,
                     ts=?
                     WHERE uuid=?"""
SELECT_ROUND = "SELECT * FROM rounds WHERE uuid=?, round=?"
INSERT_ROUND = "INSERT INTO rounds VALUES (?,?,?)"
UPDATE_ROUND = "UPDATE rounds SET user_moves=? WHERE uuid=?, round=?"
