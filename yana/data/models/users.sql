-- Create users table
CREATE TABLE IF NOT EXISTS users (
	id VARCHAR(36) PRIMARY KEY,
	first_name VARCHAR(255) NOT NULL,
	last_name VARCHAR(255) NOT NULL,
	phone_number VARCHAR(20) NOT NULL CHECK (length(phone_number) >= 10),
	gender VARCHAR(20),
	password TEXT NOT NULL,
	type VARCHAR(255) NOT NULL CHECK (type IN ("primary", "auxiliary", "professional")),
	created_at INTEGER NOT NULL,
	updated_at INTEGER NOT NULL
) WITHOUT ROWID;


-- Create triggers for automatic creation and updation timestamps (UNIX epoch)
CREATE TRIGGER set_timestamps
AFTER INSERT ON users
BEGIN
	UPDATE users
	SET
		created_at = strftime('%s', 'now'),
		updated_at = strftime('%s', 'now')
	WHERE id = new.id;
END;

CREATE TRIGGER update_timestamps
AFTER INSERT ON users
BEGIN
	UPDATE users
	SET updated_at = strftime('%s', 'now')
	WHERE id = new.id;
END;


