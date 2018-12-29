CREATE TABLE missed_chapters (
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    novel_id INT NOT NULL,
    chapter_no INT NOT NULL,
    resolved BOOLEAN NOT NULL,
    FOREIGN KEY (novel_id)
        REFERENCES novels (id)
)