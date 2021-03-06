CREATE TABLE word_count_entry (
    id SERIAL PRIMARY KEY,
    word_count INTEGER CHECK (word_count > 0 AND NOT NULL),
    date_of_entry DATE NOT NULL,
    project_title VARCHAR (100)
);
