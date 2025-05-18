class Menu:
    def run_admin_menu(self):
        print("What do you want to do ?\n")
       
        print("""1-  Add course\n2-  Edit course\n3-  delete course
4-  Add course offering\n5-  Edit course offering\n6-  delete course offering
7-  Add instructor\n8-  Edit instructor\n9-  delete instructor
10- Add student\n11- Edit student\n12- delete student\n""")
        
        try:
            choice = int(input(""))
            if choice > 12 or choice < 1:
                raise ValueError()
            print("")
            return choice
        except ValueError as e:
            print("\nInvalid Input!")
            exit(1)
    
    def run_instructor_menu(self):
        pass
    
    def run_student_menu(self):
       pass
    
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
        