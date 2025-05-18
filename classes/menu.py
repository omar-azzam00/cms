class Menu:
    def run_admin_menu(self):
        print("What do you want to do ?\n")

        print(
            """1-  Add course\n2-  Edit course\n3-  Delete course\n4-  List all courses
5-  Add course offering\n6-  Edit course offering\n7-  Delete course offering\n8-  List all course offerings
9-  Add instructor\n10- Edit instructor\n11- Delete instructor\n12- List all instructors
13- Add student\n14- Edit student\n15- Delete student\n16- List all students
17- Exit\n"""
        )

        try:
            choice = int(input(""))
            if choice > 17 or choice < 1:
                raise ValueError()
            print("")
            return choice
        except ValueError as e:
            print("\nInvalid Input!")
            exit(1)

    def run_instructor_menu(self):
        # Display the menu for instructors and get their choice
        print("\n=== Instructor Menu ===")
        print("1. View my assigned courses")
        print("2. View students in a specific course")
        print("3. Edit student grades")
        print("4. Edit my profile")

        while True:
            try:
                choice = int(input("\nEnter your choice (1-4): "))
                if 1 <= choice <= 4:
                    return choice
                else:
                    print("Invalid choice. Please enter a number between 1 and 4.")
            except ValueError:
                print("Please enter a valid number.")

    def run_student_menu(self):
        # Display the menu for students and get their choice
        print("\n=== Student Menu ===")
        print("1. View all available courses")
        print("2. View course offerings this semester")
        print("3. View my registered courses")
        print("4. Register for a course")
        print("5. Unregister from a course")
        print("6. Edit my profile")

        while True:
            try:
                choice = int(input("\nEnter your choice (1-6): "))
                if 1 <= choice <= 6:
                    return choice
                else:
                    print("Invalid choice. Please enter a number between 1 and 6.")
            except ValueError:
                print("Please enter a valid number.")

    def ask_for_id():
        print("What is your id ?\n")

        try:
            id = int(input(""))
            return id
        except ValueError as e:
            print("\nInvalid Input!")
            exit(1)

    def ask_user_type(self):
        print("Who are you ?\n")
        print("1- Admin\n2- Instructor\n3- Student\n")

        try:
            choice = int(input(""))
            if choice > 3 or choice < 1:
                raise ValueError()
            print("")
            return choice
        except ValueError as e:
            print("\nInvalid Input!")
            exit(1)
