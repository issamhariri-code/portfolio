CREATE TABLE Movies (
MovieID INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
Title VARCHAR(255) NOT NULL,
Director VARCHAR(255),
Genre VARCHAR(100),
ReleaseYear YEAR,
Rating DECIMAL(3, 1),
RuntimeMinutes SMALLINT
) ENGINE = InnoDB
DEFAULT CHARSET = utf8mb4
COLLATE = utf8mb4_swedish_ci;

INSERT INTO Movies (MovieID, Title, Director, Genre, ReleaseYear, Rating, RuntimeMinutes) VALUES
(1, 'Epic Journey', 'John Smith', 'Adventure', 1994, 9.3, 142),
(2, 'The Great Heist', 'Alice Johnson', 'Crime', 1972, 9.2, 175),
(3, 'Revolutionary Road', 'Robert Brown', 'Drama', 1974, 9.0, 202),
(4, 'Fight for Honor', 'Chris Green', 'Action', 2008, 9.0, 152),
(5, 'Galactic Battles', 'Lucy White', 'Sci-Fi', 1980, 8.9, 124),
(6, 'The Mystery of Time', 'Daniel Lee', 'Thriller', 1995, 8.9, 139),
(7, 'Legends of Tomorrow', 'Sarah Carter', 'Fantasy', 2003, 8.9, 201),
(8, 'The Last Emperor', 'Kevin Young', 'History', 1993, 8.8, 195),
(9, 'Warriors Fate', 'Rachel King', 'Action', 1994, 8.8, 154),
(10, 'Oceans Whisper', 'Gary Wilson', 'Drama', 1999, 8.8, 189),
(11, 'The Eternal City', 'Anne Taylor', 'Romance', 1946, 8.8, 104),
(12, 'Desert Mirage', 'Frank Martin', 'Adventure', 1966, 8.7, 161),
(13, 'Space Odyssey', 'Laura Garcia', 'Sci-Fi', 2012, 8.7, 148),
(14, 'The Lost Kingdom', 'Brian Davis', 'Fantasy', 2001, 8.7, 178),
(15, 'Unseen Enemy', 'Sophie Turner', 'Thriller', 1990, 8.7, 136),
(16, 'Journey Through Time', 'George Walker', 'Sci-Fi', 1985, 8.6, 116),
(17, 'Undercover Mission', 'Emily Scott', 'Action', 1979, 8.6, 127),
(18, 'The Forgotten Land', 'Michael Brown', 'Adventure', 1957, 8.6, 119),
(19, 'Road to Freedom', 'Helen Lee', 'Drama', 2006, 8.5, 133),
(20, 'Mystery of the Abyss', 'Oliver Jones', 'Mystery', 1997, 8.5, 141);


-- 1. Välj alla filmer. Lista varje rad och kolumn.

SELECT * FROM Movies;

-- 2. Filterera efter genre. Visa filmer i en genre du anger.
SELECT Title
FROM Movies
WHERE Genre = 'Action';

-- 3. Sortera efter ReleaseYear. - Visa filmer kronologiskt.

SELECT * FROM Movies
ORDER BY ReleaseYear DESC;

-- 4. Uppdatera filmdata. Ändra rating på en film.
UPDATE Movies
SET Rating = 10
WHERE MovieID = 1

-- 5. Räkna filmer per genre - Gruppera per genre och räkna antal.
SELECT Genre, COUNT(Genre)
FROM Movies
GROUP BY Genre
ORDER BY Genre;

-- 6. Hämta specifika kolumner - Lista bara Title och Director.
SELECT Title, Director FROM Movies;

-- 7. Filmer efter visst år - Välj filmer som har ReleaseYear större än valt år.
SELECT ReleaseYear
FROM Movies
WHERE ReleaseYear > 1995;

-- 8. Uppdatera flera rader - Öka RunTimeMinutes för en hel genre.
UPDATE Movies
SET RunTimeMinutes = RunTimeMinutes + 30
WHERE Genre = 'Action'

-- 9. Topprankade Filmer - Visa de fem filmer med högst rating.
SELECT Rating
FROM Movies
ORDER BY Rating DESC
LIMIT 5;

-- 10. Filmer av specifik regissör - Filtrera på en regissör du väljer.
SELECT Title
FROM Movies
WHERE Director = 'Frank Martin';


