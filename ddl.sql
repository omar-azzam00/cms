/* CREATE THE DATABASE*/
IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = 'cms')
BEGIN
    CREATE DATABASE cms;
END;

/* CREATE THE TABLES */
IF NOT EXISTS (
    SELECT * FROM sysobjects WHERE name='Instructor' AND xtype='U'
)
BEGIN
    CREATE TABLE Instructor (
        instructor_id INT IDENTITY(1,1) PRIMARY KEY,
        name VARCHAR(100),
        email VARCHAR(100),
        phone VARCHAR(15)
    );
END;

IF NOT EXISTS (
    SELECT * FROM sysobjects WHERE name='Course' AND xtype='U'
)
BEGIN
    CREATE TABLE Course (
        course_id INT IDENTITY(1,1) PRIMARY KEY,
        name VARCHAR(100),
        category VARCHAR(50),
        credits INT CHECK (credits >= 0)
    );
END;

IF NOT EXISTS (
    SELECT * FROM sysobjects WHERE name='CourseOffering' AND xtype='U'
)
BEGIN
    CREATE TABLE CourseOffering (
        offering_id INT IDENTITY(1,1) PRIMARY KEY,
        course_id INT,
        instructor_id INT,
        semester VARCHAR(10) CHECK (semester IN ('spring', 'summer', 'fall')),
        year INT,
        FOREIGN KEY (course_id) REFERENCES Course(course_id),
        FOREIGN KEY (instructor_id) REFERENCES Instructor(instructor_id)
    );
END;

IF NOT EXISTS (
    SELECT * FROM sysobjects WHERE name='Student' AND xtype='U'
)
BEGIN
    CREATE TABLE Student (
        student_id INT IDENTITY(1,1) PRIMARY KEY,
        name VARCHAR(100),
        email VARCHAR(100),
        phone VARCHAR(15),
        gpa DECIMAL(5,2) CHECK (gpa >= 0)
    );
END;

IF NOT EXISTS (
    SELECT * FROM sysobjects WHERE name='Enrollment' AND xtype='U'
)
BEGIN
    CREATE TABLE Enrollment (
        student_id INT,
        offering_id INT,
        grade DECIMAL(5,2) CHECK (grade >= 0),
        PRIMARY KEY (student_id, offering_id),
        FOREIGN KEY (student_id) REFERENCES Student(student_id),
        FOREIGN KEY (offering_id) REFERENCES CourseOffering(offering_id)
    );
END;