import os

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