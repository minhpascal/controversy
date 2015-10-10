CREATE TABLE Users (
        Id VarChar(50) Primary Key,
        Password VarChar(50) NOT NULL,
        School VarChar(50) NOT NULL,
        Name VarChar(50) NOT NULL,
	Joined TIMESTAMP,
        Logins smallint DEFAULT 0 Not NULL
);

CREATE TABLE Queries (
        Term VarChar(100),
	RatioScore float,
	EntropyScore float NOT NULL,
        Performed TIMESTAMP 
);

CREATE TABLE Histories (
        Originator VarChar(50),
        Term VarChar(100) NOT NULL,
        Performed TIMESTAMP,
        Foreign Key (Originator) References Users(Id)
);
