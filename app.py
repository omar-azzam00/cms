from classes.database import Database
from classes.menu import Menu
from classes.course_helpers import add_course
from classes.instructor_helper import add_instructor

database = Database()
menu = Menu()

print("\n")
choice = menu.ask_user_type()

if choice == 1:
    choice = menu.run_admin_menu()
    
    # Add the suitable method for each choice 
    if choice == 1:
        # Add course
        add_course(database)
    elif choice == 2:
        pass
    elif choice == 3:
        pass
    elif choice == 4:
        pass
    elif choice == 5:
        pass
    elif choice == 6:
        pass
    elif choice == 7:
        # Add Instructor
        add_instructor(database)
    elif choice == 8:
        pass
    elif choice == 9:
        pass
    elif choice == 10:
        pass
    elif choice == 11:
        pass
    else:
        pass

        
elif choice == 2:
    # validate the id before anything
    id = menu.ask_for_id()
    
    # go implement this menu at Menu class then comeback here!
    # choice = menu.run_instructor_menu()
else:
    id = menu.ask_for_id()
    
    # go implement this menu at Menu class then comeback here!
    # choice = menu.run_student_menu()

# def main_menu():
#     while True:
#         #
#         print("1: Add a new course")
#         print("2: Edit a course")
#         print("3: List the available courses")
#         print("4: Delete a course")
#         print("5: Add a new instructor")
#         print("6: Edit an instructor")
#         print("7: List the available instructors")
#         print("8: Delete an instructor")
#         print("0: Close the app")
#         choice = int(input("Enter your choice: \n"))
#         if 5 < choice < 1:
#             pass

#         if choice == 1:
#             add_course()
#         elif choice == 5:
#             from instructor_helper import add_instructor
#             add_instructor()
#         elif choice == 0:
#             break


# main_menu()

# conn.close()
