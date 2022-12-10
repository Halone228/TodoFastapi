PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

CREATE TABLE IF NOT EXISTS "group" (id INTEGER NOT NULL PRIMARY KEY, user_id INTEGER NOT NULL, title TEXT NOT NULL, color_scheme INTEGER NOT NULL, FOREIGN KEY (user_id) REFERENCES user (id) ON DELETE CASCADE);

CREATE TABLE IF NOT EXISTS todos (id INTEGER NOT NULL PRIMARY KEY, group_id INTEGER NOT NULL, title TEXT NOT NULL, text TEXT NOT NULL, deadline_time TEXT (5) NOT NULL, deadline_date TEXT (10) NOT NULL, start_time TEXT (5) NOT NULL, start_date TEXT (10) NOT NULL, status TEXT NOT NULL, FOREIGN KEY (group_id) REFERENCES "group" (id) ON DELETE CASCADE);

CREATE TABLE IF NOT EXISTS "user" ("id" INTEGER NOT NULL PRIMARY KEY, "username" TEXT NOT NULL, "password" TEXT NOT NULL);

CREATE INDEX IF NOT EXISTS group_user_id ON "group" ("user_id");

CREATE INDEX IF NOT EXISTS todos_group_id ON todos ("group_id");

CREATE UNIQUE INDEX IF NOT EXISTS "user_username" ON "user" ("username");

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
