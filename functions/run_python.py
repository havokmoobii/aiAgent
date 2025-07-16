import os
import subprocess

from google.genai import types

from functions.config import RUN_TIMEOUT

def run_python_file(working_directory, file_path):
    abs_working_directory = os.path.abspath(working_directory)
    target = os.path.abspath(os.path.join(working_directory, file_path))

    if not target.startswith(abs_working_directory):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(target):
        return f'Error: File "{file_path}" not found.'
    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    try:
        process = subprocess.run(["python", f"{file_path}"], timeout=RUN_TIMEOUT, capture_output=True, text=True, cwd=working_directory)
        if process.stdout == "" and process.stderr == "":
            return "No output produced."
        result = ""
        if process.stdout:
            result = f"STDOUT: {process.stdout}\n"
        if process.stderr:
            result += f"STDERR: {process.stderr}\n"
        if process.returncode != 0:
            result += f"Process exited with code {process.returncode}"
        return result
    
    except Exception as e:
        return f"Error: executing Python file: {e}"
    
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description=f"Attempts to use Python to execute the file at the specified file path, constrained to the working directory.",
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