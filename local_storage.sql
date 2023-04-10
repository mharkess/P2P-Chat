--
-- File generated with SQLiteStudio v3.4.3 on Sun Apr 9 20:13:32 2023
--
-- Text encoding used: System
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Table: texthistory
CREATE TABLE IF NOT EXISTS texthistory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    contents TEXT NOT NULL,
    time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
