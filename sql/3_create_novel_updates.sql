CREATE TABLE novel_updates (
    id INT NOT NULL PRIMARY KEY,
    latest_chapter INT NOT NULL,
    completed BOOLEAN NOT NULL,
    FOREIGN KEY (id)
        REFERENCES novels (id)
)

