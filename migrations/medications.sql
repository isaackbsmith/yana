-- Migration was created at 2024-07-17 17:22:30

CREATE TABLE IF NOT EXISTS medications (
	id CHAR(36) PRIMARY KEY,
	generic_name TEXT,
	brand_name TEXT NOT NULL,
	dosage_form TEXT NOT NULL,
	strength TEXT NOT NUll,
	notes TEXT
);
