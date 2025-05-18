from classes.database import Database


def add_course(database):
    """ """
    # Ask the user to enter the course data (id, name, category, credits)
    name = ""
    category = ""
    hours = 0
    while name == "":
        name = input("Enter the course name: ")

    while category == "":
        category = input("Enter the course category: ")

    while hours <= 0:
        try:
            hours = int(input("Enter the course credit hours: "))
        except ValueError as e:
            print(f"Invalid input. Please enter a number. {e}")

    insert_query = f"""
    INSERT INTO Course (name, category, credits) VALUES
    ('{name}', '{category}', {hours});
    """

    database.modify_query_execute(insert_query)

    print(f"Course {name} added successfully!")

    return


def edit_course(database):
    # Edit an existing course in the database
    print("\n=== Edit Course ===")
    course_id = input("Enter the course ID to edit: ")

    # Check if the course exists
    if not database.check_course_exists(course_id):
        print(f"Course with ID {course_id} does not exist.")
        return

    # Get current course info
    current_course = database.get_course_by_id(course_id)
    print(f"Editing course: {current_course['name']} (ID: {course_id})")

    # Get new values
    new_name = input(
        f"Enter new course name (or press Enter to keep '{current_course['name']}'): "
    )
    new_description = input(
        f"Enter new course description (or press Enter to keep current): "
    )

    # Use current values if nothing was entered
    if not new_name.strip():
        new_name = current_course["name"]
    if not new_description.strip():
        new_description = current_course["description"]

    # Update the course
    if database.update_course(course_id, new_name, new_description):
        print(f"Course {course_id} updated successfully.")
    else:
        print("Failed to update the course.")


def delete_course(database):
    # Delete a course from the database
    print("\n=== Delete Course ===")
    course_id = input("Enter the course ID to delete: ")

    # Check if the course exists
    if not database.check_course_exists(course_id):
        print(f"Course with ID {course_id} does not exist.")
        return

    # Confirm deletion
    confirm = input(
        f"Are you sure you want to delete course {course_id}? (y/n): "
    ).lower()

    if confirm == "y":
        if database.delete_course(course_id):
            print(f"Course {course_id} deleted successfully.")
        else:
            print("Failed to delete the course.")
    else:
        print("Course deletion cancelled.")


def add_course_offering(database):
    """
    Add a course offering to the database
    """
    print("\n=== Add Course Offering ===")
    course_id = input("Enter the course ID for the offering: ")

    # Check if the course exists
    if not database.check_course_exists(course_id):
        print(f"Course with ID {course_id} does not exist.")
        return

    semester = input("Enter semester (e.g., Fall 2023): ")
    instructor_id = input("Enter instructor ID: ")

    # Check if instructor exists
    if not database.check_instructor_exists(instructor_id):
        print(f"Instructor with ID {instructor_id} does not exist.")
        return

    # Add the course offering
    if database.add_course_offering(course_id, semester, instructor_id):
        print("Course offering added successfully.")
    else:
        print("Failed to add course offering.")


def edit_course_offering(database):
    """
    Edit a course offering in the database
    """
    print("\n=== Edit Course Offering ===")
    offering_id = input("Enter the course offering ID to edit: ")

    # Check if the offering exists
    if not database.check_offering_exists(offering_id):
        print(f"Course offering with ID {offering_id} does not exist.")
        return

    # Get current offering info
    current_offering = database.get_offering_by_id(offering_id)
    print(f"Editing offering: {offering_id} for course {current_offering['course_id']}")

    new_semester = input(f"Enter new semester (or press Enter to keep current): ")
    new_instructor_id = input(
        f"Enter new instructor ID (or press Enter to keep current): "
    )

    # Use current values if nothing was entered
    if not new_semester.strip():
        new_semester = current_offering["semester"]
    if not new_instructor_id.strip():
        new_instructor_id = current_offering["instructor_id"]
    elif not database.check_instructor_exists(new_instructor_id):
        print(f"Instructor with ID {new_instructor_id} does not exist.")
        return

    # Update the offering
    if database.update_course_offering(offering_id, new_semester, new_instructor_id):
        print(f"Course offering {offering_id} updated successfully.")
    else:
        print("Failed to update the course offering.")


def delete_course_offering(database):
    """
    Delete a course offering from the database
    """
    print("\n=== Delete Course Offering ===")
    offering_id = input("Enter the course offering ID to delete: ")

    # Check if the offering exists
    if not database.check_offering_exists(offering_id):
        print(f"Course offering with ID {offering_id} does not exist.")
        return

    # Confirm deletion
    confirm = input(
        f"Are you sure you want to delete course offering {offering_id}? (y/n): "
    ).lower()

    if confirm == "y":
        if database.delete_course_offering(offering_id):
            print(f"Course offering {offering_id} deleted successfully.")
        else:
            print("Failed to delete the course offering.")
    else:
        print("Course offering deletion cancelled.")


def list_courses(database):
    courses = database.get_all_courses()

    if not courses:
        print("No courses found in the database.")
        return

    print("\nCourses List:")
    print("=" * 80)
    print(f"{'ID':<10}{'Code':<15}{'Name':<30}{'Description':<25}")
    print("-" * 80)

    for course in courses:
        print(
            f"{course['id']:<10}{course['code']:<15}{course['name']:<30}{course['description']:<25}"
        )
    print("=" * 80)


def list_course_offerings(database):
    offerings = database.get_all_course_offerings()

    if not offerings:
        print("No course offerings found in the database.")
        return

    print("\nCourse Offerings List:")
    print("=" * 100)
    print(
        f"{'ID':<10}{'Course':<15}{'Semester':<15}{'Year':<10}{'Instructor':<20}{'Status':<10}"
    )
    print("-" * 100)

    for offering in offerings:
        course = database.get_course_by_id(offering["course_id"])
        instructor = (
            database.get_instructor_by_id(offering["instructor_id"])
            if offering["instructor_id"]
            else {"name": "Not Assigned"}
        )

        print(
            f"{offering['id']:<10}{course['code']:<15}{offering['semester']:<15}{offering['year']:<10}{instructor['name']:<20}{offering['status']:<10}"
        )
    print("=" * 100)
