import google.generativeai as genai
import os
import sys
from colorama import Fore, Style


def get_response(genai_chat, prompt):
    """Get a response from the Gemini API.

    Args:
        genai_chat (GenerativeChat): The Generative Chat instance.
        prompt (str): The prompt for the Gemini API.

    Returns:
        str: The content of the response.

    Raises:
        ValueError: If the response is missing content.
    """
    response = genai_chat.send_message(prompt)
    if response and hasattr(response, 'text'):
        return response.text
    raise ValueError("Missing content in response.")


def setup_gemini_api():
    """Set up the Gemini API client.

    Retrieves the Gemini API key from an environment variable and
    configures the client. If the key is not present, raises a
    ValueError.

    Raises:
        ValueError: If the API key is not present in the environment.
    """
    api_key = os.getenv("GOOGLE_GEMINI_API_KEY")
    if not api_key:
        raise ValueError("Missing GOOGLE GEMINI API Key.")
    genai.configure(api_key=api_key)


def load_code_from_file(file_path):
    """Load code from a file.

    Args:
        file_path (str): The path to the file to load.

    Returns:
        str: The content of the file.

    Raises:
        FileNotFoundError: If the file does not exist.
        PermissionError: If the file exists but cannot be read.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except (FileNotFoundError, PermissionError) as e:
        print(f"Cannot open file {file_path}: {str(e)}")
        raise


def review_code(prompt, code):
    try:
        chat = genai.GenerativeModel("gemini-1.5-flash").start_chat(history=[])
        response = get_response(chat, f"{prompt}\n```{code}```")
        return response
    except Exception as e:
        print(f"Error during code review: {e}")
        return f"Error: {e}"


def main():
    """Command-line interface for code reviewer.

    This script will take a user-defined prompt and a SQL file path
    as arguments, and print a review of the SQL code in the file
    based on the given prompt.

    Example usage:

        python code_reviewer.py "Your custom prompt here" example.sql
    """
    if len(sys.argv) < 3:
        print("Please provide a prompt and a file path.")
        sys.exit(1)

    user_prompt = sys.argv[1]
    file_path = sys.argv[2]

    setup_gemini_api()
    code = load_code_from_file(file_path)
    chat = genai.GenerativeModel(
        "gemini-1.5-flash"
    ).start_chat(history=[])

    prompt = f"{user_prompt}\n{code}"
    response = review_code(user_prompt, code)  # Call the function here

    print(
        f"{Fore.BLUE}Review {file_path}:{Fore.GREEN}\n"
        f"{response}{Style.RESET_ALL}"
    )


if __name__ == "__main__":
    main()
