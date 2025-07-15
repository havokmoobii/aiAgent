import unittest

from functions.run_python import run_python_file

class TestRunFile(unittest.TestCase):
    def test_calculator(self):
        result = run_python_file("calculator", "main.py")
        print(result + "\n")

    def test_tests(self):
        result = run_python_file("calculator", "tests.py")
        print(result + "\n")

    def test_oob(self):
        result = run_python_file("calculator", "../main.py")
        print(result + "\n")

    def test_nonexistant(self):
        result = run_python_file("calculator", "nonexistent.py")
        print(result + "\n")

if __name__ == "__main__":
    unittest.main()