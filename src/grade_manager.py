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
            print(f"{reg_no:<20}\t{name:<10}\t{grade:<10}")
        for reg_no, student_details in students.items():
            print(f"{reg_no:<20}\t{student_details['name']:<10}\t{student_details['grade']:<10}")
    else:
        print("No students found.")

def add_student():
    try:
        # Get the JSON file
        if file_exists:
            try: 
                with open(data_file, 'r') as file:
                    students = json.load(file)
            except json.JSONDecodeError as e:
                students = {}
        else:
            students = {}
        # Get the new student details
        student_name = input("Enter student name: ")
        student_grade = int(input("Enter student's grade: "))
        student_registration_no = input("Enter student's Reg.No: ")

        # Add new student to the dictionary
        students[student_registration_no] = {
            "name": student_name,
            "grade": student_grade
        }
        # updated dictionary
        with open(data_file, 'w') as file:
            json.dump(students, file, indent=4)

        print(f"Student {student_name} added successfully.")
        return True
    
    except Exception as e:
        print("An error occured. Please try again")
        return False


show_main_menu()

# Main loop
while True:
    user_option = get_user_input()

    if not validate_user_input(user_option):
        print("Invalid input! Choose an option from the menu (1-5)")
        continue
    
    if user_option == "1":
        add_student()
    elif user_option == "2":
        view_all_students()
    elif user_option == "3":
        # TODO: Implement update student grade functionality
        ...
    elif user_option == "4":
        # TODO: Implement delete student functionality
        ...
    elif user_option == "5":
        print("Exiting program. Goodbye!")
        break
