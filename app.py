from classes.database import Database
from classes.menu import Menu
from classes.course_helpers import (
    add_course,
    edit_course,
    delete_course,
    add_course_offering,
    edit_course_offering,
    delete_course_offering,
    list_courses,
    list_course_offerings,
)
from classes.instructor_helper import (
    add_instructor,
    view_assigned_courses,
    view_course_students,
    edit_student_grades,
    edit_instructor_profile,
    edit_instructor,
    delete_instructor,
    list_instructors,
)
from classes.student_helper import (
    add_student,
    edit_student,
    delete_student,
    view_all_courses,
    view_semester_offerings,
    view_registered_courses,
    register_for_course,
    unregister_from_course,
    edit_student_profile,
    list_students,
)

database = Database()
menu = Menu()

print("\n")
choice = menu.ask_user_type()

if choice == 1:
    while True:
        choice = menu.run_admin_menu()

        if choice == 17:  # Exit option (updated for new options)
            print("Exiting admin menu. Goodbye!")
            break

        # Add the suitable method for each choice
        if choice == 1:
            # Add course
            add_course(database)
        elif choice == 2:
            # Edit course
            edit_course(database)
        elif choice == 3:
            # Delete course
            delete_course(database)
        elif choice == 4:
            # List all courses
            list_courses(database)
        elif choice == 5:
            # Add course offering
            add_course_offering(database)
        elif choice == 6:
            # Edit course offering
            edit_course_offering(database)
        elif choice == 7:
            # Delete course offering
            delete_course_offering(database)
        elif choice == 8:
            # List all course offerings
            list_course_offerings(database)
        elif choice == 9:
            # Add instructor
            add_instructor(database)
        elif choice == 10:
            # Edit instructor
            edit_instructor(database)
        elif choice == 11:
            # Delete instructor
            delete_instructor(database)
        elif choice == 12:
            # List all instructors
            list_instructors(database)
        elif choice == 13:
            # Add student
            add_student(database)
        elif choice == 14:
            # Edit student
            edit_student(database)
        elif choice == 15:
            # Delete student
            delete_student(database)
        elif choice == 16:
            # List all students
            list_students(database)

elif choice == 2:
    # validate the id before anything
    instructor_id = menu.ask_for_id()

    # Validate instructor ID
    if not database.validate_instructor_id(instructor_id):
        print(f"Error: Instructor with ID {instructor_id} does not exist.")
        exit()

    while True:
        # Run instructor menu
        choice = menu.run_instructor_menu()

        if choice == 5:  # Exit option
            print("Exiting instructor menu. Goodbye!")
            break

        if choice == 1:
            # View assigned courses
            view_assigned_courses(database, instructor_id)
        elif choice == 2:
            # View students in a specific course
            view_course_students(database, instructor_id)
        elif choice == 3:
            # Edit student grades
            edit_student_grades(database, instructor_id)
        elif choice == 4:
            # Edit profile
            edit_instructor_profile(database, instructor_id)
else:
    student_id = menu.ask_for_id()

    # Validate student ID
    if not database.validate_student_id(student_id):
        print(f"Error: Student with ID {student_id} does not exist.")
        exit()

    while True:
        # Run student menu
        choice = menu.run_student_menu()

        if choice == 7:
            print("Exiting student menu. Goodbye!")
            break

        if choice == 1:
            view_all_courses(database)
        elif choice == 2:
            view_semester_offerings(database)
        elif choice == 3:
            view_registered_courses(database, student_id)
        elif choice == 4:
            register_for_course(database, student_id)
        elif choice == 5:
            unregister_from_course(database, student_id)
        elif choice == 6:
            edit_student_profile(database, student_id)
