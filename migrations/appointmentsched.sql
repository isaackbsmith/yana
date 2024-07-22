-- Migration was created at 2024-07-17 17:48:26

CREATE TABLE IF NOT EXISTS appointment_schedules (
	id CHAR(36) PRIMARY KEY,
	date INT NOT NULL,
	time INT NOT NULL,
	location TEXT NOT NULL,
	notes TEXT
);
