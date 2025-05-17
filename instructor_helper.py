from db import db_modify_query_execute, db_query_execute


def add_instructor():
    name = ""
    email = ""
    phone = ""
    while name == "":
        name = input("Enter the instructor name: ")

    while email == "":
        email = input("Enter the instructor email: ")

    while phone == "":
        phone = input("Enter the instructor phone: ")

    count_query = """SELECT COUNT(*) FROM Instructor;"""
    instructors_count = db_query_execute(count_query)

    id = instructors_count.fetchone()[0] + 1

    insert_query = f"""
    INSERT INTO Instructor (instructor_id, name, email, phone) VALUES
    ({id}, '{name}', '{email}', '{phone}');
    """

    db_modify_query_execute(insert_query)

    print(f"Instructor {name} added successfully!")

    return
