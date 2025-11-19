--Nybörjaruppgifter i SQL
-- Skapat av : Issam Adam Hariri
-- Skriven i Dbeaver med databas MariaDB, pushad till repo via VScode terminal

CREATE TABLE products (
	ProductID INT PRIMARY KEY,
	ProductName VARCHAR(255),
	Price DECIMAL(10, 2)
	);

INSERT INTO Products (ProductID, ProductName, Price)
VALUES (232, 'Samsung S25', 9190.00);
INSERT INTO Products (ProductID, ProductName, Price)
VALUES (211, 'Iphone 16', 7299.00);
INSERT INTO Products (ProductID, ProductName, Price)
VALUES (155, 'Iphone 14', 4999.00);

SELECT * FROM Products

SELECT Price
FROM Products;

SELECT Price
FROM Products
WHERE Price > 50;

SELECT *
FROM Products
ORDER BY Price DESC;

SELECT COUNT(*)
FROM Products;

UPDATE Products
SET Price = 8999.00
WHERE ProductID = 211;

DELETE FROM Products
WHERE ProductID = 155;

ALTER TABLE Products
ADD Stock INT;