import os

from google.genai import types

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
    
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description=f"Reads the up to {MAX_CHARS} of the content of a file at the specified file path, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path, relative to the working directory, where the file is located.",
            ),
        },
    ),
)