create_users = """CREATE TABLE IF NOT EXISTS users(
                   username VARCHAR PRIMARY KEY,
                   password VARCHAR NOT NULL)"""

create_sessions = """CREATE TABLE IF NOT EXISTS sessions(
                      uuid VARCHAR PRIMARY KEY,
                      users VARCHAR NOT NULL,
                      payload VARCHAR NOT NULL,
                      state VARCHAR NOT NULL,
                      ts INT NOT NULL)"""

select_user    = "SELECT * FROM users WHERE username=?"
insert_user    = "INSERT INTO users VALUES (?, ?)"
select_session = "SELECT * FROM sessions WHERE uuid=?"
insert_session = "INSERT INTO sessions VALUES (?,?,?,?,?)"
update_session = "UPDATE sessions SET users=?, payload=?, state=?, ts=? WHERE uuid=?"
