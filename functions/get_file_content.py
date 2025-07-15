import os

from functions.config import MAX_CHARS

def get_file_content(working_directory, file_path):
    abs_working_directory = os.path.abspath(working_directory)
    target = os.path.abspath(os.path.join(working_directory, file_path))

    if not target.startswith(abs_working_directory):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(target):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    try:
        with open(target, "r") as f:
          result = f.read(MAX_CHARS)
        if os.path.getsize(target) > MAX_CHARS:
            result += f' [...File "{file_path}" truncated at {MAX_CHARS} characters]'
        return result
    except Exception as e:
        return f"Error: {e}"