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
                      payload VARCHAR NOT NULL,
                      state VARCHAR NOT NULL,
                      ts INT NOT NULL)"""

SELECT_USER = "SELECT * FROM users WHERE username=?"
INSERT_USER = "INSERT INTO users VALUES (?, ?)"
SELECT_SESSION = "SELECT * FROM sessions WHERE uuid=?"
INSERT_SESSION = "INSERT INTO sessions VALUES (?,?,?,?,?)"
UPDATE_SESSION = "UPDATE sessions SET users=?, payload=?, state=?, ts=? WHERE uuid=?"
