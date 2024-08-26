-- schedules Generated on 2024-08-26 11:56:41.447948

-- Entity table
CREATE TABLE IF NOT EXISTS schedules (
    id VARCHAR(36) PRIMARY KEY,
    begin_date INTEGER NOT NULL,
    end_date INTEGER NOT NULL,
    begin_time INTEGER NOT NULL,
    end_time INTEGER NOT NULL,
    -- No check contraint on the schedule type
    -- It's possible there might be variants that
    -- are not accounted for which will require a
    -- table migration
    schedule_type VARCHAR(255),
    repeated VARCHAR(255) CHECK (repeated IN (
        'minutely',
        'hourly',
        'daily',
        'weekly',
        'monthly',
        'annually'
    )),
    repetition_step INTEGER,
    repeated_monthly_on VARCHAR(255) CHECK (repeated_monthly_on IN (
        'same_day',
        'same_weekday'
    )),
    repeated_until VARCHAR(255) CHECK (repeated_until IN (
        'forever',
        'until_date',
        'n_repetitions'
    )),
    repeated_until_date INTEGER,
    repeated_reps INTEGER,
    user_id VARCHAR(36),
    medication_id VARCHAR(36),
    appointment_id VARCHAR(36),
    created_at INTEGER NOT NULL,
    updated_at INTEGER NOT NULL,
    FOREIGN KEY (user_id)
        REFERENCES users (id)
            ON DELETE CASCADE
            ON UPDATE CASCADE,
    FOREIGN KEY (medication_id)
        REFERENCES medications (id)
            ON DELETE SET NULL
            ON UPDATE CASCADE,
    FOREIGN KEY (appointment_id)
        REFERENCES appointments (id)
            ON DELETE SET NULL
            ON UPDATE CASCADE
) WITHOUT ROWID;


-- Triggers for automatic creation and updation timestamps (UNIX epoch)
CREATE TRIGGER set_schedules_timestamps
AFTER INSERT ON schedules
BEGIN
    UPDATE schedules
    SET
        created_at = strftime('%s', 'now'),
        updated_at = strftime('%s', 'now')
    WHERE id = new.id;
END;

CREATE TRIGGER update_schedules_timestamps
AFTER INSERT ON schedules
BEGIN
    UPDATE schedules
    SET updated_at = strftime('%s', 'now')
    WHERE id = new.id;
END;
