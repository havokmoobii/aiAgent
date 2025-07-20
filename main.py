import os
import sys
import types

from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.get_files_info import get_files_info, schema_get_files_info
from functions.get_file_content import get_file_content, schema_get_file_content
from functions.write_file import write_file, schema_write_file
from functions.run_python import run_python_file, schema_run_python_file


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

If the user does not specify file names look for files with simular names.

If the user asks you to fix a bug check the .py files for the source of the bug and correct it.
"""
    for i in range(20):
        try:
            response = client.models.generate_content(
                model='gemini-2.0-flash-001',
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions], system_instruction=system_prompt
                    )
                )
            for candidate in response.candidates:
                messages.append(candidate.content)

            function_calls = response.function_calls
            if function_calls:
                for function_call in function_calls:
                    function_call_result = call_function(function_call, verbose)
                    messages.append(function_call_result)
                    if function_call_result.parts[0].function_response.response:
                        if verbose:
                            print(f"-> {function_call_result.parts[0].function_response.response}")
                    else:
                        raise Exception("Fatal Error: No string response from call_function")
            else:
                print(response.text)
                break
        except Exception as e:
            print(e)
            break
    
    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else: print(f"Calling function: {function_call_part.name}")

    functions = {"get_files_info": get_files_info,
                 "get_file_content": get_file_content,
                 "write_file": write_file,
                 "run_python_file": run_python_file}
    
    function_call_part.args['working_directory'] = "./calculator"
    
    if function_call_part.name in functions:
        function_result = functions[function_call_part.name](**function_call_part.args)
        return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_call_part.name,
                response={"result": function_result},
                )
            ],
        )
    else:
        return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_call_part.name,
                response={"error": f"Unknown function: {function_call_part.name}"},
                )
            ],
        )
    

if __name__ == "__main__":
    main()
