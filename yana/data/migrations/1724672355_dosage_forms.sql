-- dosage_forms Generated on 2024-08-26 11:39:15.839539

-- Entity table
CREATE TABLE IF NOT EXISTS dosage_forms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) UNIQUE NOT NULL,
    friendly_name VARCHAR(255),
    description TEXT,
    created_at INTEGER,
    updated_at INTEGER
);


-- Triggers for automatic creation and updation timestamps (UNIX epoch)
CREATE TRIGGER set_dosage_forms_timestamps
AFTER INSERT ON dosage_forms
BEGIN
    UPDATE dosage_forms
    SET
        created_at = strftime('%s', 'now'),
        updated_at = strftime('%s', 'now')
    WHERE id = NEW.id;
END;

CREATE TRIGGER update_dosage_forms_timestamps
AFTER INSERT ON dosage_forms
BEGIN
    UPDATE dosage_forms
    SET updated_at = strftime('%s', 'now')
    WHERE id = NEW.id;
END;
