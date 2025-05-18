def add_student(database):
    """
    Add a new student to the database
    """
    print("\n=== Add Student ===")
    student_id = input("Enter student ID: ")

    # Check if student already exists
    if database.check_student_exists(student_id):
        print(f"Student with ID {student_id} already exists.")
        return

    name = input("Enter student name: ")
    email = input("Enter student email: ")

    # Add the student
    if database.add_student(student_id, name, email):
        print(f"Student {name} added successfully with ID: {student_id}")
    else:
        print("Failed to add student.")


def edit_student(database):
    """
    Edit an existing student in the database
    """
    print("\n=== Edit Student ===")
    student_id = input("Enter the student ID to edit: ")

    # Check if the student exists
    if not database.check_student_exists(student_id):
        print(f"Student with ID {student_id} does not exist.")
        return

    # Get current student info
    current_student = database.get_student_by_id(student_id)
    print(f"Editing student: {current_student['name']} (ID: {student_id})")

    # Get new values
    new_name = input(
        f"Enter new name (or press Enter to keep '{current_student['name']}'): "
    )
    new_email = input(f"Enter new email (or press Enter to keep current): ")

    # Use current values if nothing was entered
    if not new_name.strip():
        new_name = current_student["name"]
    if not new_email.strip():
        new_email = current_student["email"]

    # Update the student
    if database.update_student(student_id, new_name, new_email):
        print(f"Student {student_id} updated successfully.")
    else:
        print("Failed to update the student.")


def delete_student(database):
    """
    Delete a student from the database
    """
    print("\n=== Delete Student ===")
    student_id = input("Enter the student ID to delete: ")

    # Check if the student exists
    if not database.check_student_exists(student_id):
        print(f"Student with ID {student_id} does not exist.")
        return

    # Confirm deletion
    confirm = input(
        f"Are you sure you want to delete student {student_id}? (y/n): "
    ).lower()

    if confirm == "y":
        if database.delete_student(student_id):
            print(f"Student {student_id} deleted successfully.")
        else:
            print("Failed to delete the student.")
    else:
        print("Student deletion cancelled.")


def view_all_courses(database):
    # Display all available courses in the system
    print("\n=== All Available Courses ===")
    courses = database.get_all_courses()

    if not courses:
        print("No courses available in the system.")
        return

    print("ID\tCourse Name\tDescription")
    print("-" * 60)
    for course in courses:
        print(f"{course['id']}\t{course['name']}\t{course['description']}")


def view_semester_offerings(database):
    # Display all course offerings available in the current semester
    print("\n=== Course Offerings This Semester ===")

    # Get current semester from user
    current_semester = input("Enter the current semester (e.g., Fall 2023): ")

    offerings = database.get_semester_offerings(current_semester)

    if not offerings:
        print(f"No course offerings available for {current_semester}.")
        return

    print("ID\tCourse Name\tInstructor\tSemester")
    print("-" * 70)
    for offering in offerings:
        print(
            f"{offering['id']}\t{offering['course_name']}\t{offering['instructor_name']}\t{offering['semester']}"
        )


def view_registered_courses(database, student_id):
    """
    Display all courses that the student is registered for
    """
    print("\n=== My Registered Courses ===")
    courses = database.get_student_courses(student_id)

    if not courses:
        print("You are not registered for any courses.")
        return

    print("ID\tCourse Name\tSemester\tInstructor\tGrade")
    print("-" * 80)
    for course in courses:
        grade = course["grade"] if course["grade"] is not None else "N/A"
        print(
            f"{course['offering_id']}\t{course['course_name']}\t{course['semester']}\t{course['instructor_name']}\t{grade}"
        )


def register_for_course(database, student_id):
    """
    Register a student for a course
    """
    print("\n=== Register for a Course ===")

    # Show available course offerings
    print("Available course offerings:")
    offerings = database.get_available_offerings(student_id)

    if not offerings:
        print("No available course offerings to register for.")
        return

    print("ID\tCourse Name\tInstructor\tSemester")
    print("-" * 70)
    for offering in offerings:
        print(
            f"{offering['id']}\t{offering['course_name']}\t{offering['instructor_name']}\t{offering['semester']}"
        )

    offering_id = input(
        "\nEnter the ID of the course offering you want to register for (or 0 to cancel): "
    )
    if offering_id == "0":
        return

    # Check if the offering exists and student is not already registered
    if not database.check_offering_exists(offering_id):
        print("Invalid offering ID.")
        return

    if database.check_student_registered(student_id, offering_id):
        print("You are already registered for this course.")
        return

    # Register the student
    if database.register_student(student_id, offering_id):
        print("Successfully registered for the course.")
    else:
        print("Failed to register for the course.")


def unregister_from_course(database, student_id):
    """
    Unregister a student from a course
    """
    print("\n=== Unregister from a Course ===")

    # Show registered courses
    courses = database.get_student_courses(student_id)

    if not courses:
        print("You are not registered for any courses.")
        return

    print("Your registered courses:")
    print("ID\tCourse Name\tSemester")
    print("-" * 60)
    for course in courses:
        print(f"{course['offering_id']}\t{course['course_name']}\t{course['semester']}")

    offering_id = input(
        "\nEnter the ID of the course offering you want to unregister from (or 0 to cancel): "
    )
    if offering_id == "0":
        return

    # Check if the student is registered for this course
    if not database.check_student_registered(student_id, offering_id):
        print("You are not registered for this course.")
        return

    # Confirm unregistration
    confirm = input(
        "Are you sure you want to unregister from this course? (y/n): "
    ).lower()
    if confirm != "y":
        print("Unregistration cancelled.")
        return

    # Unregister the student
    if database.unregister_student(student_id, offering_id):
        print("Successfully unregistered from the course.")
    else:
        print("Failed to unregister from the course.")


def edit_student_profile(database, student_id):
    """
    Allow student to edit their own profile (email or phone)
    """
    print("\n=== Edit My Profile ===")

    # Get current student info
    student = database.get_student_by_id(student_id)
    if not student:
        print("Student information not found.")
        return

    print(f"Current information:")
    print(f"Name: {student['name']}")
    print(f"Email: {student['email']}")
    print(f"Phone: {student.get('phone', 'Not provided')}")

    print("\nWhat would you like to update?")
    print("1. Email")
    print("2. Phone")
    print("3. Both")
    print("4. Cancel")

    try:
        choice = int(input("\nEnter your choice (1-4): "))

        if choice == 4:
            return

        new_email = student["email"]
        new_phone = student.get("phone", "")

        if choice in [1, 3]:
            new_email = input("Enter new email: ")

        if choice in [2, 3]:
            new_phone = input("Enter new phone: ")

        if database.update_student_contact(student_id, new_email, new_phone):
            print("Profile updated successfully.")
        else:
            print("Failed to update profile.")
    except ValueError:
        print("Please enter a valid number.")


def list_students(database):
    """List all students in the database"""
    students = database.get_all_students()

    if not students:
        print("No students found in the database.")
        return

    print("\nStudents List:")
    print("=" * 100)
    print(f"{'ID':<10}{'Name':<30}{'Email':<30}{'Major':<20}{'GPA':<10}")
    print("-" * 100)

    for student in students:
        print(
            f"{student['id']:<10}{student['name']:<30}{student['email']:<30}{student['major']:<20}{student['gpa']:<10}"
        )
    print("=" * 100)
