import json
from pathlib import Path
import os

current_path = Path(__file__).resolve().parent
project_root = current_path.parent
data_file = project_root/"data"/"students.json"
file_exists = os.path.exists(data_file)

def show_main_menu():
    print("==Student grade manager==")
    print("Please choose an option: ")
    print("""
    1. Add a new student
    2. View all students
    3. Update a student's grade
    4. Delete a student
    5. Exit
    """)

def get_user_input():
    return input("Pick an option (1-5): ")

def is_duplicate(reg_no, students):
    return reg_no in students

def open_file():
    try:
        with open(data_file, 'r') as file:
            students = json.load(file)
            if not isinstance(students, dict):
                students = {}
    except Exception:
        print("Could not load file")
        students = {}
    return students

def validate_user_input(input):
    if input in ("1", "2", "3", "4", "5"):
        return True
    return False

def view_all_students():
    # Load JSON file
    try:
        with open(data_file, 'r') as file:
            students = json.load(file)
            if not isinstance(students, dict):
                students = {}
    except Exception:
        print("Could not load file")
        students = {}
    
    if students:
        for reg_no, student_details in students.items():
            name = student_details.get('name', 'N/A')
            grade = student_details.get('grade', 'N/A')
            print(f"{reg_no.upper():<20}\t{name:<10}\t{grade:<10}")
        for reg_no, student_details in students.items():
            print(f"{reg_no.upper():<20}\t{student_details['name']:<10}\t{student_details['grade']:<10}")
    else:
        print("No students found.")

def add_student():
    try:
        students = open_file()
        # Get the new student details
        student_name = input("Enter student name: ")
        student_grade = int(input("Enter student's grade: "))
        student_registration_no = input("Enter student's Reg.No: ").upper()

        # Prevent duplicate ID using cached students
        if is_duplicate(student_registration_no, students):
            print("Student already exists!")
            return False
        else:
            # Add new student to the dictionary
            students[student_registration_no] = {
                "name": student_name,
                "grade": student_grade
            }
            # updated dictionary
            with open(data_file, 'w') as file:
                json.dump(students, file, indent=4, sort_keys=True)

            print(f"Student {student_name} added successfully.")
            return True
    
    except Exception as e:
        print("An error occured. Please try again")
        return False

def update_student():
    reg_no = input("Enter student registration number: ").upper()
    try:
        with open(data_file, "r") as file:
            students = json.load(file)
        if reg_no not in students:
            print("Error! Registration number not found!")
            return
        else:
            print("Update details")
            name = input("Update new name: ")
            grade = int(input("Update new grade: "))

            students[reg_no] = {
                "name": name,
                "grade": grade
            }
            with open(data_file, "w") as file:
                json.dump(students, file, indent=4, sort_keys=True)
            print("Success")
            return
    except Exception as e:
        print(f"An error occured: {e}")
        return False

def delete_student():
    reg_no = input("Enter the reg no of the student you want to delete: ").upper()
    try:
        students = open_file()
        if reg_no not in students:
            print("Error! Registration number not found!")
            return
        del students[reg_no]
        with open(data_file, "w") as file:
            json.dump(students, file, indent=4, sort_keys=True)
        print("Success")
        return
    except Exception as e:
        print(f"An error occured: {e}")
        return False

show_main_menu()

# Cache students dictionary
students_cache = open_file()

# Main loop
while True:
    user_option = get_user_input()

    if not validate_user_input(user_option):
        print("Invalid input! Choose an option from the menu (1-5)")
        continue
    
    if user_option == "1":
        # Update cache if student is added
        if add_student():
            students_cache = open_file()
    elif user_option == "2":
        view_all_students()
    elif user_option == "3":
        update_student()
        students_cache = open_file()
    elif user_option == "4":
        delete_student()
        students_cache = open_file()
    elif user_option == "5":
        print("Exiting program. Goodbye!")
        break
