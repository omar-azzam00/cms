from database import Database

def add_course(database):
    """ """
    # Ask the user to enter the course data (id, name, category, credits)
    name = ""
    category = ""
    hours = 0
    instructor_id = 0
    while name == "":
        name = input("Enter the course name: ")

    while category == "":
        category = input("Enter the course category: ")

    while hours <= 0:
        try:
            hours = int(input("Enter the course credit hours: "))
        except ValueError as e:
            print(f"Invalid input. Please enter a number. {e}")

    while instructor_id <= 0:
        try:
            instructor_id = int(input("Enter the course instructor id: "))
        except ValueError as e:
            print(f"Invalid input. Please enter a id. {e}")

    count_query = """SELECT COUNT(*) FROM Course;"""

    courses_count = database.query_execute(count_query)

    id = courses_count.fetchone()[0] + 1
    print(f"New course id: {id}")

    insert_query = f"""
    INSERT INTO Course (course_id, name, category, credits, instructor_id) VALUES
    ({id}, '{name}', '{category}', {hours}, {instructor_id});
    """

    database.modify_query_execute(insert_query)

    print(f"Course {name} added successfully!")

    return

