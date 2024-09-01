-- adherence_slots Generated on 2024-08-26 12:38:20.947614

-- Entity table
CREATE TABLE IF NOT EXISTS adherence_slots (
    id VARCHAR(36) PRIMARY KEY,
    date INTEGER NOT NULL,
    time INTEGER NOT NULL,
    adherence_status VARCHAR(255) CHECK (adherence_status IN (
        'fully_adherent',
        'partially_adherent',
        'not_adherent',
        'temporarily_exempt',
        'not_relevant'
    )),
    adherence_time INTEGER NOT NULL,
    reminder_status VARCHAR(255) CHECK (reminder_status IN (
        'pending',
        'sent',
        'acknowledged',
        'overdue',
        'completed'
    )),
    non_adherence_reason TEXT,
    notes TEXT,
    schedule_id VARCHAR(36),
    created_at INTEGER,
    updated_at INTEGER,
    FOREIGN KEY (schedule_id)
        REFERENCES schedules (id)
            ON DELETE SET NULL
            ON UPDATE CASCADE
) WITHOUT ROWID;


-- Triggers for automatic creation and updation timestamps (UNIX epoch)
CREATE TRIGGER set_adherence_slots_timestamps
AFTER INSERT ON adherence_slots
BEGIN
    UPDATE adherence_slots
    SET
        created_at = strftime('%s', 'now'),
        updated_at = strftime('%s', 'now')
    WHERE id = NEW.id;
END;

CREATE TRIGGER update_adherence_slots_timestamps
AFTER INSERT ON adherence_slots
BEGIN
    UPDATE adherence_slots
    SET updated_at = strftime('%s', 'now')
    WHERE id = NEW.id;
END;
