-- Migration was created at 2024-07-17 17:38:25

CREATE TABLE IF NOT EXISTS medication_adherence (
	id CHAR(36) PRIMARY KEY,
	schedule_id CHAR(36) NOT NULL,
	scheduled_datetime INT NOT NULL,
	actual_datetime INT NOT NULL,
	adherence_status BOOLEAN,
	reminder_status BOOLEAN,
	non_adherence_reason TEXT,
	notes TEXT,
	FOREIGN KEY (schedule_id) REFERENCES medication_schedules (id)
);
