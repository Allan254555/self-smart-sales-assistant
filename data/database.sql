
CREATE TABLE categories(
	CategoryID INT PRIMARY KEY,
	CategoryName VARCHAR(100) NOT NULL
);
CREATE TABLE products(
	ProductID INT PRIMARY KEY,
	ProductNAME VARCHAR(150) NOT NULL,
	CategoryID INT,
	Class VARCHAR(10),
	ModifyDate TIMESTAMP,
	Resistant VARCHAR(20),
	IsAllergic VARCHAR(20),
	VitalityDays INT,
	Price NUMERIC(10,2),
	FOREIGN KEY (CategoryID) REFERENCES categories(CategoryID)
);
CREATE TABLE countries(
	CountryID INT PRIMARY KEY,
	CountryName VARCHAR(100) NOT NULL,
	CountryCode Varchar(4)
);
CREATE TABLE cities(
	CityID INT PRIMARY KEY,
	CityName VARCHAR(100) NOT NULL,
	Zipcode INT,
	CountryID INT,
	FOREIGN KEY (CountryID) REFERENCES countries(countryID)
);
CREATE TABLE customers(
	CustomerID INT PRIMARY KEY,
	FirstName VARCHAR(200) NOT NULL,
	MiddleInitial CHAR(1),
	LastName VARCHAR(100) NOT NULL,
	CityID INT,
	Address VARCHAR(200),
	FOREIGN KEY (CityID) REFERENCES cities(CityID)
	
);
CREATE TABLE employees(
	EmployeeID INT PRIMARY KEY,
	FirstName VARCHAR(200) NOT NULL,
	MiddleInitial CHAR(1),
	LastName VARCHAR(200) NOT NULL,
	BirthDate TIMESTAMP,
	Gender CHAR(1),
	CityID INT,
	HireDate TIMESTAMP,
	FOREIGN KEY (CityID) REFERENCES cities(CityID)
);
CREATE TABLE sales (
    SalesID INT PRIMARY KEY, 
	SalesPersonID INT,
	CustomerID INT,
    ProductID INT,
    Quantity INT,
	Discount NUMERIC(5,2)DEFAULT 0.00,
	TotalPrice NUMERIC(12,2),
   	SalesDate TIMESTAMP NOT NULL,
   	TransactionNumber VARCHAR(50) UNIQUE,
    FOREIGN KEY (ProductID) REFERENCES products(ProductID),
    FOREIGN KEY (CustomerID) REFERENCES customers(CustomerID),
    FOREIGN KEY (SalesPersonID) REFERENCES employees(EmployeeID)
);