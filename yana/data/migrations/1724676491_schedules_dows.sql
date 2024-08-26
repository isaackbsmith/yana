-- schedules_dows Generated on 2024-08-26 12:48:11.473412

-- Entity table
CREATE TABLE IF NOT EXISTS schedules_dows (
    schedule_id VARCHAR(36),
    day_of_week VARCHAR(20),
    created_at INTEGER NOT NULL,
    updated_at INTEGER NOT NULL,
    PRIMARY KEY (schedule_id, day_of_week)
) WITHOUT ROWID;


-- Triggers for automatic creation and updation timestamps (UNIX epoch)
CREATE TRIGGER set_schedules_dows_timestamps
AFTER INSERT ON schedules_dows
BEGIN
    UPDATE schedules_dows
    SET
        created_at = strftime('%s', 'now'),
        updated_at = strftime('%s', 'now')
    WHERE id = new.id;
END;

CREATE TRIGGER update_schedules_dows_timestamps
AFTER INSERT ON schedules_dows
BEGIN
    UPDATE schedules_dows
    SET updated_at = strftime('%s', 'now')
    WHERE id = new.id;
END;
