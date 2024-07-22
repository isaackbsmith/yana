-- Migration was created at 2024-07-17 17:14:07

CREATE TABLE IF NOT EXISTS users (
	id CHAR(36) PRIMARY KEY,
	first_name VARCHAR(255) NOT NULL,
	last_name VARCHAR(255) NOT NULL,
	phone_number VARCHAR(20) NOT NULL,
	gender VARCHAR(100) NOT NULL,
	date_of_birth INT NOT NULL,
	role TEXT CHECK(role IN ('PRIMARY', 'AUXILLIARY', 'PROFESSIONAL'))
);
