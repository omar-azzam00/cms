import pyodbc
from dotenv import load_dotenv
from os import environ


class Database:
    def __init__(self):
        self.__connect()
        self.__create_db()

    def query_execute(self, query):
        try:
            self.cursor.execute(query)
            return self.cursor
        except Exception as e:
            print(f"An error accorded: {e}")

    def modify_query_execute(self, query):
        try:
            self.cursor.execute(query)
            self.conn.commit()
        except Exception as e:
            print(f"An error accorded: {e}")
            self.conn.rollback()

    def __connect(self):
        DRIVER = environ.get("DRIVER")
        SERVER = environ.get("SERVER")

        conn_str = f"Driver={DRIVER};Server={SERVER};Trusted_Connection=yes;"

        try:
            self.conn = pyodbc.connect(conn_str)
            self.cursor = self.conn.cursor()
            # print("Connection successful!")
        except Exception as e:
            print(f"Error connecting to database: {e}")

    def __create_db(self):
        try:
            ddl_file = open("./extras/ddl.sql")
            ddl = ddl_file.read()
            self.cursor.execute(ddl)

        except FileNotFoundError as e:
            print("Please Include the correct path for the ddl.sql file")
            print(e)
        except Exception as e:
            print("Error while executing ddl!", e)

    def get_instructor_by_id(self, instructor_id):
        # Retrieve instructor information by ID
        query = f"SELECT * FROM instructors WHERE id = '{instructor_id}'"
        try:
            cursor = self.query_execute(query)
            instructor = cursor.fetchone()

            if instructor:
                return {
                    "id": instructor[0],
                    "name": instructor[1],
                    "email": instructor[2],
                    "phone": instructor[3] if len(instructor) > 3 else None,
                }
        except Exception as e:
            print(f"Error retrieving instructor: {e}")
        return None

    def get_instructor_courses(self, instructor_id):
        # Get all courses assigned to an instructor
        query = """
            SELECT co.id as offering_id, c.name as course_name, co.semester
            FROM course_offerings co
            JOIN courses c ON co.course_id = c.id
            WHERE co.instructor_id = ?
        """
        try:
            # Fix: Replace placeholder properly without nested f-strings
            formatted_query = query.replace("?", f"'{instructor_id}'")
            cursor = self.query_execute(formatted_query)
            courses = cursor.fetchall()

            result = []
            for course in courses:
                result.append(
                    {
                        "offering_id": course[0],
                        "course_name": course[1],
                        "semester": course[2],
                    }
                )
            return result
        except Exception as e:
            print(f"Error retrieving instructor courses: {e}")
            return []

    def get_students_in_course(self, offering_id):
        # Get all students enrolled in a specific course offering
        query = """
            SELECT s.id as student_id, s.name, s.email, e.grade
            FROM enrollments e
            JOIN students s ON e.student_id = s.id
            WHERE e.offering_id = ?
        """
        try:
            # Fix: Replace placeholder properly without nested f-strings
            formatted_query = query.replace("?", f"'{offering_id}'")
            cursor = self.query_execute(formatted_query)
            students = cursor.fetchall()

            result = []
            for student in students:
                result.append(
                    {
                        "student_id": student[0],
                        "name": student[1],
                        "email": student[2],
                        "grade": student[3],
                    }
                )
            return result
        except Exception as e:
            print(f"Error retrieving students in course: {e}")
            return []

    def update_student_grade(self, student_id, offering_id, grade):
        # Update a student's grade in a specific course
        try:
            query = f"""
                UPDATE enrollments 
                SET grade = '{grade}' 
                WHERE student_id = '{student_id}' AND offering_id = '{offering_id}'
            """
            self.modify_query_execute(query)
            return True
        except Exception as e:
            print(f"Error updating grade: {e}")
            return False

    def update_student_gpa(self, student_id):
        # Update a student's GPA based on all their grades
        try:
            # Get all grades for the student
            query = f"SELECT grade FROM enrollments WHERE student_id = '{student_id}' AND grade IS NOT NULL"
            cursor = self.query_execute(query)
            grades = cursor.fetchall()

            if not grades:
                return True  # No grades to calculate GPA

            # Calculate GPA (assuming 4.0 scale)
            total_grade = 0
            count = 0

            for grade in grades:
                numeric_grade = grade[0]
                if numeric_grade is not None:
                    count += 1
                    # Convert percentage to GPA (simplified)
                    if numeric_grade >= 90:
                        gpa_points = 4.0
                    elif numeric_grade >= 80:
                        gpa_points = 3.0
                    elif numeric_grade >= 70:
                        gpa_points = 2.0
                    elif numeric_grade >= 60:
                        gpa_points = 1.0
                    else:
                        gpa_points = 0.0
                    total_grade += gpa_points

            if count > 0:
                gpa = total_grade / count
            else:
                gpa = 0

            # Update the student's GPA
            update_query = f"UPDATE students SET gpa = {gpa} WHERE id = '{student_id}'"
            self.modify_query_execute(update_query)
            return True
        except Exception as e:
            print(f"Error updating GPA: {e}")
            return False

    def update_instructor_contact(self, instructor_id, email, phone):
        # Update instructor's contact information
        try:
            query = f"""
                UPDATE instructors 
                SET email = '{email}', phone = '{phone}' 
                WHERE id = '{instructor_id}'
            """
            self.modify_query_execute(query)
            return True
        except Exception as e:
            print(f"Error updating instructor info: {e}")
            return False

    def validate_instructor_id(self, instructor_id):
        # Check if an instructor ID exists in the database
        query = f"SELECT id FROM instructors WHERE id = '{instructor_id}'"
        cursor = self.query_execute(query)
        result = cursor.fetchone()
        return result is not None

    def get_all_courses(self):
        # Get all courses in the system
        query = "SELECT id, name, description FROM courses"
        try:
            cursor = self.query_execute(query)
            courses = cursor.fetchall()

            result = []
            for course in courses:
                result.append(
                    {"id": course[0], "name": course[1], "description": course[2]}
                )
            return result
        except Exception as e:
            print(f"Error retrieving courses: {e}")
            return []

    def get_semester_offerings(self, semester):
        # Get all course offerings for a specific semester
        query = f"""
            SELECT co.id, c.name as course_name, i.name as instructor_name, co.semester
            FROM course_offerings co
            JOIN courses c ON co.course_id = c.id
            JOIN instructors i ON co.instructor_id = i.id
            WHERE co.semester = '{semester}'
        """
        try:
            cursor = self.query_execute(query)
            offerings = cursor.fetchall()

            result = []
            for offering in offerings:
                result.append(
                    {
                        "id": offering[0],
                        "course_name": offering[1],
                        "instructor_name": offering[2],
                        "semester": offering[3],
                    }
                )
            return result
        except Exception as e:
            print(f"Error retrieving semester offerings: {e}")
            return []

    def get_student_courses(self, student_id):
        # Get all courses a student is registered for
        query = f"""
            SELECT co.id as offering_id, c.name as course_name, co.semester, 
                i.name as instructor_name, e.grade
            FROM enrollments e
            JOIN course_offerings co ON e.offering_id = co.id
            JOIN courses c ON co.course_id = c.id
            JOIN instructors i ON co.instructor_id = i.id
            WHERE e.student_id = '{student_id}'
        """
        try:
            cursor = self.query_execute(query)
            courses = cursor.fetchall()

            result = []
            for course in courses:
                result.append(
                    {
                        "offering_id": course[0],
                        "course_name": course[1],
                        "semester": course[2],
                        "instructor_name": course[3],
                        "grade": course[4],
                    }
                )
            return result
        except Exception as e:
            print(f"Error retrieving student courses: {e}")
            return []

    def get_available_offerings(self, student_id):
        # Get all course offerings a student is not already registered for
        query = f"""
            SELECT co.id, c.name as course_name, i.name as instructor_name, co.semester
            FROM course_offerings co
            JOIN courses c ON co.course_id = c.id
            JOIN instructors i ON co.instructor_id = i.id
            WHERE co.id NOT IN (
                SELECT offering_id FROM enrollments WHERE student_id = '{student_id}'
            )
        """
        try:
            cursor = self.query_execute(query)
            offerings = cursor.fetchall()

            result = []
            for offering in offerings:
                result.append(
                    {
                        "id": offering[0],
                        "course_name": offering[1],
                        "instructor_name": offering[2],
                        "semester": offering[3],
                    }
                )
            return result
        except Exception as e:
            print(f"Error retrieving available offerings: {e}")
            return []

    def check_offering_exists(self, offering_id):
        # Check if a course offering exists
        query = f"SELECT id FROM course_offerings WHERE id = '{offering_id}'"
        cursor = self.query_execute(query)
        result = cursor.fetchone()
        return result is not None

    def check_student_registered(self, student_id, offering_id):
        # Check if a student is already registered for a course offering
        query = f"SELECT * FROM enrollments WHERE student_id = '{student_id}' AND offering_id = '{offering_id}'"
        cursor = self.query_execute(query)
        result = cursor.fetchone()
        return result is not None

    def register_student(self, student_id, offering_id):
        # Register a student for a course offering
        try:
            query = f"INSERT INTO enrollments (student_id, offering_id) VALUES ('{student_id}', '{offering_id}')"
            self.modify_query_execute(query)
            return True
        except Exception as e:
            print(f"Error registering student: {e}")
            return False

    def unregister_student(self, student_id, offering_id):
        # Unregister a student from a course offering
        try:
            query = f"DELETE FROM enrollments WHERE student_id = '{student_id}' AND offering_id = '{offering_id}'"
            self.modify_query_execute(query)
            return True
        except Exception as e:
            print(f"Error unregistering student: {e}")
            return False

    def get_student_by_id(self, student_id):
        # Get student information by ID
        query = f"SELECT id, name, email, phone FROM students WHERE id = '{student_id}'"
        try:
            cursor = self.query_execute(query)
            student = cursor.fetchone()

            if student:
                return {
                    "id": student[0],
                    "name": student[1],
                    "email": student[2],
                    "phone": student[3] if len(student) > 3 else None,
                }
            return None
        except Exception as e:
            print(f"Error retrieving student info: {e}")
            return None

    def update_student_contact(self, student_id, email, phone):
        # Update student's contact information
        try:
            query = f"UPDATE students SET email = '{email}', phone = '{phone}' WHERE id = '{student_id}'"
            self.modify_query_execute(query)
            return True
        except Exception as e:
            print(f"Error updating student contact: {e}")
            return False

    def validate_student_id(self, student_id):
        # Check if a student ID exists in the database
        query = f"SELECT id FROM students WHERE id = '{student_id}'"
        cursor = self.query_execute(query)
        result = cursor.fetchone()
        return result is not None
