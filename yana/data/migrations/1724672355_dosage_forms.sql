-- dosage_forms Generated on 2024-08-26 11:39:15.839539

-- Entity table
CREATE TABLE IF NOT EXISTS dosage_forms (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    friendly_name VARCHAR(255),
    created_at INTEGER NOT NULL,
    updated_at INTEGER NOT NULL
) WITHOUT ROWID;


-- Triggers for automatic creation and updation timestamps (UNIX epoch)
CREATE TRIGGER set_dosage_forms_timestamps
AFTER INSERT ON dosage_forms
BEGIN
    UPDATE dosage_forms
    SET
        created_at = strftime('%s', 'now'),
        updated_at = strftime('%s', 'now')
    WHERE id = new.id;
END;

CREATE TRIGGER update_dosage_forms_timestamps
AFTER INSERT ON dosage_forms
BEGIN
    UPDATE dosage_forms
    SET updated_at = strftime('%s', 'now')
    WHERE id = new.id;
END;
