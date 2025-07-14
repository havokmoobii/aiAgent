import unittest

from functions.get_file_content import get_file_content

class TestGetFileContent(unittest.TestCase):
    def test_main(self):
        result = get_file_content("calculator", "main.py")
        print(result + "\n")

    def test_calculator(self):
        result = get_file_content("calculator", "pkg/calculator.py")
        print(result + "\n")

    def test_cat(self):
        result = get_file_content("calculator", "/bin/cat")
        print(result + "\n")

if __name__ == "__main__":
    unittest.main()