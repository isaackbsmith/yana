-- Migration was created at 2024-07-17 17:50:28


CREATE TABLE IF NOT EXISTS appointment_adherence (
	id CHAR(36) PRIMARY KEY,
	schedule_id CHAR(36),
	adherence_status BOOLEAN,
	reminder_status BOOLEAN,
	non_adherence_reason TEXT,
	notes TEXT,
	FOREIGN KEY (schedule_id) REFERENCES appointment_schedules (id)
);
