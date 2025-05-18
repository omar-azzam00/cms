from classes.database import Database


def add_instructor(database):
    name = ""
    email = ""
    phone = ""
    while name == "":
        name = input("Enter the instructor name: ")

    while email == "":
        email = input("Enter the instructor email: ")

    while phone == "":
        phone = input("Enter the instructor phone: ")

    insert_query = f"""
    INSERT INTO Instructor (name, email, phone) VALUES
    ('{name}', '{email}', '{phone}');
    """

    database.modify_query_execute(insert_query)

    print(f"Instructor {name} added successfully!")

    return


def edit_instructor(database):
    # Edit an existing instructor in the database
    print("\n=== Edit Instructor ===")
    instructor_id = input("Enter the instructor ID to edit: ")

    # Check if the instructor exists
    if not database.check_instructor_exists(instructor_id):
        print(f"Instructor with ID {instructor_id} does not exist.")
        return

    # Get current instructor info
    current_instructor = database.get_instructor_by_id(instructor_id)
    print(f"Editing instructor: {current_instructor['name']} (ID: {instructor_id})")

    # Get new values
    new_name = input(
        f"Enter new name (or press Enter to keep '{current_instructor['name']}'): "
    )
    new_email = input(f"Enter new email (or press Enter to keep current): ")

    # Use current values if nothing was entered
    if not new_name.strip():
        new_name = current_instructor["name"]
    if not new_email.strip():
        new_email = current_instructor["email"]

    # Update the instructor
    if database.update_instructor(instructor_id, new_name, new_email):
        print(f"Instructor {instructor_id} updated successfully.")
    else:
        print("Failed to update the instructor.")


def delete_instructor(database):
    # Delete an instructor from the database
    print("\n=== Delete Instructor ===")
    instructor_id = input("Enter the instructor ID to delete: ")

    # Check if the instructor exists
    if not database.check_instructor_exists(instructor_id):
        print(f"Instructor with ID {instructor_id} does not exist.")
        return

    # Confirm deletion
    confirm = input(
        f"Are you sure you want to delete instructor {instructor_id}? (y/n): "
    ).lower()

    if confirm == "y":
        if database.delete_instructor(instructor_id):
            print(f"Instructor {instructor_id} deleted successfully.")
        else:
            print("Failed to delete the instructor.")
    else:
        print("Instructor deletion cancelled.")


def view_assigned_courses(database, instructor_id):
    # Display all courses assigned to the instructor
    print("\n=== My Assigned Courses ===")
    courses = database.get_instructor_courses(instructor_id)

    if not courses:
        print("You don't have any assigned courses.")
        return

    print("ID\tCourse Name\tSemester")
    print("-" * 40)
    for course in courses:
        print(f"{course['offering_id']}\t{course['course_name']}\t{course['semester']}")


def view_course_students(database, instructor_id):
    # Display all students enrolled in a specific course taught by this instructor
    print("\n=== View Students in Course ===")

    # First, show the instructor their courses
    courses = database.get_instructor_courses(instructor_id)
    if not courses:
        print("You don't have any assigned courses.")
        return

    print("Your courses:")
    for idx, course in enumerate(courses, 1):
        print(
            f"{idx}. {course['course_name']} - {course['semester']} (ID: {course['offering_id']})"
        )

    try:
        selection = int(input("\nSelect a course number: "))
        if 1 <= selection <= len(courses):
            selected_course = courses[selection - 1]
            offering_id = selected_course["offering_id"]

            # Get students in the selected course
            students = database.get_students_in_course(offering_id)

            if not students:
                print(
                    f"No students are enrolled in {selected_course['course_name']} - {selected_course['semester']}."
                )
                return

            print(
                f"\nStudents enrolled in {selected_course['course_name']} - {selected_course['semester']}:"
            )
            print("ID\tName\tEmail\tGrade")
            print("-" * 60)
            for student in students:
                grade = student["grade"] if student["grade"] is not None else "N/A"
                print(
                    f"{student['student_id']}\t{student['name']}\t{student['email']}\t{grade}"
                )
        else:
            print("Invalid selection.")
    except ValueError:
        print("Please enter a valid number.")


def edit_student_grades(database, instructor_id):
    # Edit grades for students in a course taught by this instructor
    print("\n=== Edit Student Grades ===")

    # First, show the instructor their courses
    courses = database.get_instructor_courses(instructor_id)
    if not courses:
        print("You don't have any assigned courses.")
        return

    print("Your courses:")
    for idx, course in enumerate(courses, 1):
        print(
            f"{idx}. {course['course_name']} - {course['semester']} (ID: {course['offering_id']})"
        )

    try:
        selection = int(input("\nSelect a course number: "))
        if 1 <= selection <= len(courses):
            selected_course = courses[selection - 1]
            offering_id = selected_course["offering_id"]

            # Get students in the selected course
            students = database.get_students_in_course(offering_id)

            if not students:
                print(
                    f"No students are enrolled in {selected_course['course_name']} - {selected_course['semester']}."
                )
                return

            print(
                f"\nStudents enrolled in {selected_course['course_name']} - {selected_course['semester']}:"
            )
            for idx, student in enumerate(students, 1):
                grade = student["grade"] if student["grade"] is not None else "N/A"
                print(
                    f"{idx}. {student['name']} (ID: {student['student_id']}) - Current Grade: {grade}"
                )

            student_selection = int(
                input("\nSelect a student number to update grade (0 to cancel): ")
            )
            if student_selection == 0:
                return
            if 1 <= student_selection <= len(students):
                selected_student = students[student_selection - 1]
                student_id = selected_student["student_id"]

                current_grade = (
                    selected_student["grade"]
                    if selected_student["grade"] is not None
                    else "N/A"
                )
                print(f"Current grade for {selected_student['name']}: {current_grade}")

                try:
                    new_grade = float(input("Enter new grade (0-100): "))
                    if 0 <= new_grade <= 100:
                        if database.update_student_grade(
                            student_id, offering_id, new_grade
                        ):
                            print(
                                f"Grade updated successfully for {selected_student['name']}."
                            )
                            # Update GPA
                            database.update_student_gpa(student_id)
                            print("Student GPA has been automatically updated.")
                        else:
                            print("Failed to update grade.")
                    else:
                        print("Grade must be between 0 and 100.")
                except ValueError:
                    print("Please enter a valid number for the grade.")
            else:
                print("Invalid student selection.")
        else:
            print("Invalid course selection.")
    except ValueError:
        print("Please enter a valid number.")


def edit_instructor_profile(database, instructor_id):
    # Allow instructor to edit their own profile (email or phone)
    print("\n=== Edit My Profile ===")

    # Get current instructor info
    instructor = database.get_instructor_by_id(instructor_id)
    if not instructor:
        print("Instructor information not found.")
        return

    print(f"Current information:")
    print(f"Name: {instructor['name']}")
    print(f"Email: {instructor['email']}")
    print(f"Phone: {instructor.get('phone', 'Not provided')}")

    print("\nWhat would you like to update?")
    print("1. Email")
    print("2. Phone")
    print("3. Both")
    print("4. Cancel")

    try:
        choice = int(input("\nEnter your choice (1-4): "))

        if choice == 4:
            return

        new_email = instructor["email"]
        new_phone = instructor.get("phone", "")

        if choice in [1, 3]:
            new_email = input("Enter new email: ")

        if choice in [2, 3]:
            new_phone = input("Enter new phone: ")

        if database.update_instructor_contact(instructor_id, new_email, new_phone):
            print("Profile updated successfully.")
        else:
            print("Failed to update profile.")
    except ValueError:
        print("Please enter a valid number.")


def list_instructors(database):
    """List all instructors in the database"""
    instructors = database.get_all_instructors()

    if not instructors:
        print("No instructors found in the database.")
        return

    print("\nInstructors List:")
    print("=" * 90)
    print(f"{'ID':<10}{'Name':<30}{'Email':<30}{'Phone':<20}")
    print("-" * 90)

    for instructor in instructors:
        print(
            f"{instructor['id']:<10}{instructor['name']:<30}{instructor['email']:<30}{instructor['phone']:<20}"
        )
    print("=" * 90)
