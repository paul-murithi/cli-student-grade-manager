import unittest
import os
import json
from src.grade_manager import (
    data_file,
    file_exists,
    show_main_menu,
    get_user_input,
    is_duplicate,
    open_file,
    validate_user_input,
    view_all_students,
    add_student,
    update_student_grade,
    delete_student,
)

class TestGradeManager(unittest.TestCase):
    def setUp(self):
        # Create temporary data file for testing
        self.test_data_file = 'test_students.json'
        global data_file
        data_file = self.test_data_file
        with open(self.test_data_file, 'w') as f:
            json.dump({}, f)

    def tearDown(self):
        # Remove the temporary data file after tests
        if os.path.exists(self.test_data_file):
            os.remove(self.test_data_file)

    def test_file_exists(self):
        self.assertTrue(file_exists)
        os.remove(self.test_data_file)
        self.assertFalse(os.path.exists(data_file))

    def test_show_main_menu(self):
        # Runs without error
        try:
            show_main_menu()
        except Exception as e:
            self.fail(f"show_main_menu() raised an exception {e}")

    def test_get_user_input(self):
        # Mock input to test function
        import builtins
        original_input = builtins.input
        builtins.input = lambda _: '1'
        self.assertEqual(get_user_input(), '1')
        builtins.input = original_input

    def test_is_duplicate(self):
        students = {'123': {'name': 'Alice', 'grade': 90}}
        self.assertTrue(is_duplicate('123', students))
        self.assertFalse(is_duplicate('456', students))

    def test_open_file(self):
        students = open_file()
        self.assertIsInstance(students, dict)
        self.assertEqual(students, {})

    def test_validate_user_input(self):
        self.assertTrue(validate_user_input('1'))
        self.assertTrue(validate_user_input('5'))
        self.assertFalse(validate_user_input('0'))
        self.assertFalse(validate_user_input('6'))
        self.assertFalse(validate_user_input('a'))

    def test_view_all_students_empty(self):
        # Capture output
        from io import StringIO
        import sys
        captured_output = StringIO()
        sys.stdout = captured_output
        view_all_students()
        sys.stdout = sys.__stdout__
        self.assertIn("No students found.", captured_output.getvalue())

    def test_add_student(self):
        import builtins
        original_input = builtins.input
        inputs = iter(['123', 'Alice', '90'])
        builtins.input = lambda _: next(inputs)
        
        add_student()
        
        students = open_file()
        self.assertIn('123', students)
        self.assertEqual(students['123']['name'], 'Alice')
        self.assertEqual(students['123']['grade'], 90)
        builtins.input = original_input