import os

from google.genai import types

def get_files_info(working_directory, directory=None):
    abs_working_directory = os.path.abspath(working_directory)
    result = f"Result for '{directory}' directory:"
    target = abs_working_directory

    if directory:
        target = os.path.abspath(os.path.join(working_directory, directory))
    if not target.startswith(abs_working_directory):
        result += f'\n\tError: Cannot list "{directory}" as it is outside the permitted working directory'
        return result
    if not os.path.isdir(target):
        result += f'\n\tError: "{directory}" is not a directory'
        return result
    try:
        contents = os.listdir(target)
        for item in contents:
            item_path = f"{target}/{item}"
            file_size = os.path.getsize(item_path)
            is_dir = os.path.isdir(item_path)
            result += f"\n - {item}: file_size={file_size} bytes, is_dir={is_dir}"
        return result
    except Exception as e:
        return f"Error listing files: {e}"
    
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)
