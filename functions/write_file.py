import os

from google.genai import types

def write_file(working_directory, file_path, content):
    abs_working_directory = os.path.abspath(working_directory)
    target = os.path.abspath(os.path.join(working_directory, file_path))

    if not target.startswith(abs_working_directory):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    try:
        if "/" in target:
            split_path = target.split("/")
            target_directory = "/".join(split_path[:-1])
            print(target_directory)
            if not os.path.exists(target_directory):
                os.makedirs(target_directory)
        with open(target, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"
    
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description=f"Overwrites the contents of a file at the specified file path, constrained to the working directory. The file is overwritten with new content passed to the function.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path, relative to the working directory, where the file is located.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="New text or code that will replace the file's original contents.",
            ),
        },
    ),
)