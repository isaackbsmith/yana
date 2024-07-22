-- Migration was created at 2024-07-17 18:04:20


CREATE TABLE IF NOT EXISTS medication_schedules (
	id CHAR(30) PRIMARY KEY,
	user_id CHAR(36) NOT NULL,
	medication_id CHAR(30) NOT NULL,
	frequency_id CHAR(30) NOT NULL,
	user_preferred_name TEXT,
	start_date INT NOT NULL,
	end_date INT,
	notes TEXT,
	FOREIGN KEY (user_id) REFERENCES users (id),
	FOREIGN KEY (medication_id) REFERENCES medications (id),
	FOREIGN KEY (frequency_id) REFERENCES medication_frequencies (id)
);
