-- medication_routes Generated on 2024-08-26 11:36:56.780324

-- Entity table
CREATE TABLE IF NOT EXISTS medication_routes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) UNIQUE NOT NULL,
    friendly_name VARCHAR(255),
    description TEXT,
    created_at INTEGER,
    updated_at INTEGER
);


-- Triggers for automatic creation and updation timestamps (UNIX epoch)
CREATE TRIGGER set_medication_routes_timestamps
AFTER INSERT ON medication_routes
BEGIN
    UPDATE medication_routes
    SET
        created_at = strftime('%s', 'now'),
        updated_at = strftime('%s', 'now')
    WHERE id = NEW.id;
END;

CREATE TRIGGER update_medication_routes_timestamps
AFTER INSERT ON medication_routes
BEGIN
    UPDATE medication_routes
    SET updated_at = strftime('%s', 'now')
    WHERE id = NEW.id;
END;
