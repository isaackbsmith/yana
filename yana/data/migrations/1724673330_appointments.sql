-- appointments Generated on 2024-08-26 11:55:30.823277

-- Entity table
CREATE TABLE IF NOT EXISTS appointments (
    id CHAR(36) PRIMARY KEY,
    reason TEXT NOT NULL,
    location TEXT,
    -- user_id VARCHAR(36),
    created_at INTEGER,
    updated_at INTEGER
    -- FOREIGN KEY (user_id)
    --     REFERENCES users (id)
    --         ON DELETE CASCADE
    --         ON UPDATE CASCADE
) WITHOUT ROWID;


-- Triggers for automatic creation and updation timestamps (UNIX epoch)
CREATE TRIGGER set_appointments_timestamps
AFTER INSERT ON appointments
BEGIN
    UPDATE appointments
    SET
        created_at = strftime('%s', 'now'),
        updated_at = strftime('%s', 'now')
    WHERE id = NEW.id;
END;

CREATE TRIGGER update_appointments_timestamps
AFTER INSERT ON appointments
BEGIN
    UPDATE appointments
    SET updated_at = strftime('%s', 'now')
    WHERE id = NEW.id;
END;
