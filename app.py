from db import conn
from course_helpers import add_course


def main_menu():
    while True:
        #
        print("1: Add a new course")
        print("2: Edit a course")
        print("3: List the available courses")
        print("4: Delete a course")
        print("5: Add a new instructor")
        print("6: Edit an instructor")
        print("7: List the available instructors")
        print("8: Delete an instructor")
        print("0: Close the app")
        choice = int(input("Enter your choice: \n"))
        if 5 < choice < 1:
            pass

        if choice == 1:
            add_course()
        elif choice == 5:
            from instructor_helper import add_instructor
            add_instructor()
        elif choice == 0:
            break


main_menu()

conn.close()
