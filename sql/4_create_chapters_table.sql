CREATE TABLE chapters (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    novelId INT NOT NULL,
    chapterNo INT NOT NULL,
    chapter TEXT NOT NULL,
    FOREIGN KEY (novelId)
        REFERENCES novels (id)
)

