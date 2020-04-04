CREATE TABLE IF NOT EXISTS posts (
    post_id INTEGER PRIMARY KEY AUTOINCREMENT,
    post_author INTEGER NOT NULL,   -- save author id
    post_title  TEXT    NOT NULL,
    post_content    TEXT    NOT NULL,
    post_date   DATETIME    NOT NULL,
    tag INTEGER,
    attachment  TEXT    NOT NULL,
    views   INTEGER NOT NULL    DEFAULT 0
);

CREATE TABLE IF NOT EXISTS tags (
    tag_id  INTEGER PRIMARY KEY AUTOINCREMENT,
    tag_name    TEXT    NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    password    TEXT    NOT NULL,
    email   TEXT    NOT NULL,
    role   INTEGER DEFAULT 0  -- save role id
);

-- admin can custom in the future
CREATE TABLE IF NOT EXISTS user_roles (
    role_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    permission  INTEGER DEFAULT 1,
);

-- record all permissions for customing user roles
CREATE TABLE IF NOT EXISTS user_permissions (
    permission_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    permission  TEXT
);