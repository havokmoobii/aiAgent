import unittest

from functions.write_file import write_file

class TestWriteFile(unittest.TestCase):
    def test_lorem(self):
        result = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
        print(result + "\n")

    def test_morelorem(self):
        result = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
        print(result + "\n")

    def test_temp_oob(self):
        result = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
        print(result + "\n")

if __name__ == "__main__":
    unittest.main()