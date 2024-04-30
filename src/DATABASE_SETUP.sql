CREATE DATABASE GDE;

CREATE TABLE Professor (
    ID INT PRIMARY KEY,
    NAME VARCHAR(255)
);

CREATE TABLE Subject (
    ID INT PRIMARY KEY,
    SubjectName VARCHAR(255)
);

-- ! CHANGE FROM INT TO FLOATS
CREATE TABLE ProfessorRankings (
    ProfessorID INT,
    SubjectID INT,
    OverallRanking INT,
    Coerente INT,
    ExplicaBem INT,
    Facilidade INT,
    FOREIGN KEY (ProfessorID) REFERENCES Professor(ID),
    FOREIGN KEY (SubjectID) REFERENCES Subject(ID)
);
