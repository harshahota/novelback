CREATE TABLE novels (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    label VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    sourceid INT NOT NULL,
    with_books BOOLEAN,
    FOREIGN KEY (sourceid)
        REFERENCES sources (id)
)

