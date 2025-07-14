import unittest

from functions.get_files_info import get_files_info

class TestGetFilesInfo(unittest.TestCase):
    def test_calculator_to_calculator(self):
        result = get_files_info("calculator", ".")
        print(result + "\n")

    def test_calculator_to_pkg(self):
        result = get_files_info("calculator", "pkg")
        print(result + "\n")

    def test_calculator_to_bin(self):
        result = get_files_info("calculator", "/bin")
        print(result + "\n")

    def test_calculator_to_root(self):
        result = get_files_info("calculator", "../")
        print(result + "\n")

if __name__ == "__main__":
    unittest.main()