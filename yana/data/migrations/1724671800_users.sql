-- users Generated on 2024-08-26 11:30:00.105445

-- Entity table
CREATE TABLE IF NOT EXISTS users (
    id VARCHAR(36) PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    email TEXT,
    phone_number VARCHAR(20) NOT NULL CHECK (length(phone_number) >= 10),
    gender VARCHAR(20),
    password TEXT NOT NULL,
    user_type VARCHAR(255) NOT NULL CHECK (user_type IN ("primary", "auxiliary", "professional")),
    created_at INTEGER,
    updated_at INTEGER
) WITHOUT ROWID;


-- Triggers for automatic creation and updation timestamps (UNIX epoch)
CREATE TRIGGER set_users_timestamps
AFTER INSERT ON users
BEGIN
    UPDATE users
    SET
        created_at = strftime('%s', 'now'),
        updated_at = strftime('%s', 'now')
    WHERE id = NEW.id;
END;

CREATE TRIGGER update_users_timestamps
AFTER INSERT ON users
BEGIN
    UPDATE users
    SET updated_at = strftime('%s', 'now')
    WHERE id = NEW.id;
END;
