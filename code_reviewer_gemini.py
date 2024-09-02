import google.generativeai as genai
import os
import sys
from colorama import Fore, Style


def get_response(genai_chat, prompt):
    """
    Get a response from the Gemini API.

    Args:
        genai_chat (GenerativeChat): The Generative Chat instance.
        prompt (str): The prompt for the Gemini API.

    Returns:
        str: The content of the response.
    """
    response = genai_chat.send_message(prompt)
    if response and hasattr(response, 'text'):
        return response.text
    else:
        raise ValueError("Missing content in response.")


def setup_gemini_api():
    api_key = os.getenv("GOOGLE_GEMINI_API_KEY")
    if not api_key:
        raise ValueError("Missing GOOGLE GEMINI API Key.")
    genai.configure(api_key=api_key)


def load_code_from_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except (FileNotFoundError, PermissionError) as e:
        print(f"Cannot open file {file_path}: {str(e)}")
        raise


def main():
    if len(sys.argv) < 2:
        print("Please provide a file path.")
        sys.exit(1)

    setup_gemini_api()
    code = load_code_from_file(sys.argv[1])
    chat = genai.GenerativeModel("gemini-1.5-flash").start_chat(history=[])

    prompt = (
        f"Berikan Review pada file database query ini dalam bahasa indonesia"
        f"berikan suggestion, improvement, analisis waktu eksekusi, feedback"
        f"penggunaan indeks, optimasi pengambilan data"
        f"penggunaan limit dan offset:\n{code}"
    )

    response = get_response(chat, prompt)

    print(
        f"{Fore.BLUE}Review {sys.argv[1]}:{Fore.GREEN}\n{response}{Style.RESET_ALL}"
    )


if __name__ == "__main__":
    main()
