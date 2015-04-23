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

CREATE TABLE Articles (
        Query VarChar(100) Not Null,
        Title VarChar(200) Not Null,
        Author VarChar(100) Not Null,
        Published Time Not Null,
        Url VarChar(50) Not Null,
        Source VarChar(50) Not Null,
        Abstract Text,
        Whole Text,
        Xlarge VarChar(100),
        Foreign Key (Query) References Queries(Term)
);

CREATE TABLE Tweets (
        Query VarChar(100) Not Null,
        Author VarChar(100) Not Null,
        Pimg VarChar(150) Not Null,
        Followers SMALLINT Not Null,
        Tweet VarChar(200) Not Null,
        Clean VarChar(200) Not Null,
        Published Date Not Null,
        Sentiment VarChar(15) Not Null,
        Foreign Key (Query) References Queries(Term)
);
