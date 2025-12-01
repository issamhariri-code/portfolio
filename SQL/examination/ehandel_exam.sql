CREATE TABLE Products (
	ProductID INT PRIMARY KEY,
	Name VARCHAR (100),
	Price DECIMAL(10,2),
	Category VARCHAR(50)
	);

CREATE TABLE Orders (
 OrderID INT PRIMARY KEY,
 ProductID INT,
 Quantity INT,
 OrderDate DATE,
 FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
);

CREATE TABLE Customers (
	CustomerID INT PRIMARY KEY,
	FirstName VARCHAR(100),
	LastName VARCHAR(100),
	Email VARCHAR(100),
	Phone VARCHAR(100)
	);

ALTER TABLE Orders
ADD COLUMN CustomerID INT;

ALTER TABLE Orders
ADD CONSTRAINT fk_orders_customers 
FOREIGN KEY (CustomerID)
REFERENCES Customers(CustomerID);

INSERT INTO Products(ProductID, Name, Price, Category)
	VALUES
	(1, 'Iphone 17', 1599.00, 'Phone'),
	(2, 'Samsung TV', 6999.00, 'Television'),
	(3, 'Playstation 5', 5999.00, 'Gaming'),
	(4, 'JBL Speakers', 3999.00, 'Sound'),
	(5, 'Sony Camera', 2999.00, 'Graphics');

INSERT INTO Customers (CustomerID, FirstName, LastName, Email, Phone)
	VALUES
	(1, 'Johan', 'Falk', 'johan.falk@hotmail.com', '0705647624'),
	(2, 'Seth', 'Rydell', 'seth.rydell@hotmail.com', '0706532341'),
	(3, 'Frank', 'Wagner', 'frank.wagner@hotmail.com', '0708997649'),
	(4, 'Patrick', 'Agrell', 'patrick.agrell@hotmail.com', '0709962458'),
	(5, 'Conny', 'Lindblad', 'conny.lindblad@hotmail.com', '0704311234');

INSERT INTO Orders (OrderID, ProductID, CustomerID, Quantity, OrderDate)
	VALUES
	(1, 4, 1, 3, '2025-08-11'),
	(2, 1, 2, 1, '2025-09-23'),
	(3, 2, 3, 2, '2025-06-07'),
	(4, 3, 4, 1, '2025-04-20'),
	(5, 5, 5, 4, '2025-07-20');

SELECT OrderID, Name, Quantity, OrderDate
FROM Orders
JOIN Products
ON Orders.ProductID = Products.ProductID;

SELECT OrderID, FirstName, LastName, OrderDate, Quantity
FROM Orders
JOIN Customers
ON Orders.CustomerID = Customers.CustomerID;

SELECT FirstName, LastName, Name, Quantity, OrderDate
FROM Orders
JOIN Customers
ON Orders.CustomerID = Customers.CustomerID
JOIN Products 
ON Orders.ProductID = Products.ProductID;
-- vilken kund köpte vilken produkt? hur mycket och när?

CREATE PROCEDURE GetOrdersForCustomer(IN customer_id INT)
BEGIN
    SELECT FirstName, LastName, Name, Quantity, OrderDate
    FROM Orders
    JOIN Customers
      ON Orders.CustomerID = Customers.CustomerID
    JOIN Products 
      ON Orders.ProductID = Products.ProductID
    WHERE Customers.CustomerID = customer_id;
END;

SELECT FirstName, LastName, Name, Quantity, OrderDate
FROM Orders
JOIN Customers
ON Orders.CustomerID = Customers.CustomerID
JOIN Products 
ON Orders.ProductID = Products.ProductID;

CREATE INDEX idx_orders_customerid
ON Orders(CustomerID);


CALL GetOrdersForCustomer(3) ;

USE ehandel;

EXPLAIN SELECT * FROM Orders
WHERE CustomerID = 3;

CREATE VIEW CustomerOrderView AS
SELECT FirstName, LastName, Name, Quantity, OrderDate
FROM Orders
JOIN Customers
ON Orders.CustomerID = Customers.CustomerID
JOIN Products 
ON Orders.ProductID = Products.ProductID;

SELECT * FROM CustomerOrderView;

CREATE USER 'ehandel_user'@'%' IDENTIFIED BY 'ehandel123';
GRANT SELECT ON ehandel.* TO 'ehandel_user'@'%';

INSERT INTO Products (ProductID, Name, Price, Category)
VALUES (999, 'Test', 1.00, 'Test');
-- test insert för att se att ehandel_user inte kan göra ändringar

SELECT * FROM Products;


DELETE FROM Products
WHERE ProductID = 999;









DROP TABLE IF EXISTS `customerorderview`;

SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8mb4;
/*!50001 CREATE VIEW `customerorderview` AS SELECT
 1 AS `FirstName`,
  1 AS `LastName`,
  1 AS `Name`,
  1 AS `Quantity`,
  1 AS `OrderDate` */;
SET character_set_client = @saved_cs_client;
