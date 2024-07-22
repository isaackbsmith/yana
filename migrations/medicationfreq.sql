-- Migration was created at 2024-07-17 17:25:38

CREATE TABLE IF NOT EXISTS medication_frequencies (
	id CHAR(36) PRIMARY KEY,
	frequency TEXT NOT NULL,
	times_of_day TEXT NOT NULL
);
