-- schedules_dows Generated on 2024-08-26 12:48:11.473412

-- Entity table
CREATE TABLE IF NOT EXISTS schedules_dows (
    schedule_id VARCHAR(36),
    day_of_week VARCHAR(3),
    created_at INTEGER,
    updated_at INTEGER,
    PRIMARY KEY (schedule_id, day_of_week),
    FOREIGN KEY (schedule_id) REFERENCES schedules (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
) WITHOUT ROWID;


-- Triggers for automatic creation and updation timestamps (UNIX epoch)
CREATE TRIGGER set_schedules_dows_timestamps
AFTER INSERT ON schedules_dows
BEGIN
    UPDATE schedules_dows
    SET
        created_at = strftime('%s', 'now'),
        updated_at = strftime('%s', 'now')
    WHERE id = NEW.id;
END;

CREATE TRIGGER update_schedules_dows_timestamps
AFTER INSERT ON schedules_dows
BEGIN
    UPDATE schedules_dows
    SET updated_at = strftime('%s', 'now')
    WHERE id = NEW.id;
END;
