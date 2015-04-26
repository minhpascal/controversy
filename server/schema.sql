CREATE TABLE Users (
        Id VarChar(50) Primary Key,
        Password VarChar(50) Not Null,
        School VarChar(50) Not Null,
        Name VarChar(50) Not Null
);

CREATE TABLE Queries (
        Term VarChar(100) Primary Key,
        Performed Time Not Null
);

CREATE TABLE Histories (
        Originator VarChar(50),
        Term VarChar(100) Not Null,
        Performed VarChar(20) Not Null,
        Foreign Key (Originator) References Users(Id)
);

-- tweets and articles are now stored in redis
