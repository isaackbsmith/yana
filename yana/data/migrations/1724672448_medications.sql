-- medications Generated on 2024-08-26 11:40:48.335057

-- Entity table
CREATE TABLE IF NOT EXISTS medications (
    id CHAR(36) PRIMARY KEY,
    brand_name VARCHAR(255) NOT NULL,
    generic_name VARCHAR(255),
    description TEXT,
    strength VARCHAR(20),
    -- user_id VARCHAR(36),
    dosage VARCHAR(255),
    dosage_form_id VARCHAR(36),
    medication_route_id VARCHAR(36),
    created_at INTEGER,
    updated_at INTEGER,
    -- FOREIGN KEY (user_id)
    --     REFERENCES users (id)
    --         ON DELETE CASCADE
    --         ON UPDATE CASCADE,
    FOREIGN KEY (dosage_form_id)
        REFERENCES dosage_forms (id)
            ON DELETE SET NULL
            ON UPDATE CASCADE,
    FOREIGN KEY (medication_route_id)
        REFERENCES medication_routes (id)
            ON DELETE SET NULL
            ON UPDATE CASCADE
) WITHOUT ROWID;


-- Triggers for automatic creation and updation timestamps (UNIX epoch)
CREATE TRIGGER set_medications_timestamps
AFTER INSERT ON medications
BEGIN
    UPDATE medications
    SET
        created_at = strftime('%s', 'now'),
        updated_at = strftime('%s', 'now')
    WHERE id = NEW.id;
END;

CREATE TRIGGER update_medications_timestamps
AFTER INSERT ON medications
BEGIN
    UPDATE medications
    SET updated_at = strftime('%s', 'now')
    WHERE id = NEW.id;
END;
