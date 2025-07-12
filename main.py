import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types



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

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]
    response = client.models.generate_content(
        model='gemini-2.0-flash-001', contents=messages
    )
    print(response.text)

    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

if __name__ == "__main__":
    main()
