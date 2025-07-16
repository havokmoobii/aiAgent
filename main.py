import os
import sys
import types

from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_python import schema_run_python_file


def main():
    load_dotenv()

    if len(sys.argv) == 1:
        print("aiAgent")
        print("This program requires a text prompt to be submitted as a command line argument.")
        print('Usage: uv run main.py "Prompt goes here" (Optional)Keyword arguments')
        print("Keyword arguments: --verbose: Includes user prompt and token usage.")
        exit(1)

    verbose = False
    if len(sys.argv) > 2:
        if sys.argv[2] == "--verbose":
            verbose = True

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    user_prompt = sys.argv[1]
    if verbose:
        print(f"User prompt: {user_prompt}\n")

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_write_file,
            schema_run_python_file,
        ]
    )

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]
    system_prompt = system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""
    response = client.models.generate_content(
        model='gemini-2.0-flash-001',
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
)
    )
    function_calls = response.function_calls
    if function_calls:
        for function_call in function_calls:
            print(f"Calling function: {function_call.name}({function_call.args})")
    else:
        print(response.text)
    
    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

if __name__ == "__main__":
    main()
