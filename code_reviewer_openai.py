import os
import sys

from colorama import init, Fore, Back, Style
import openai

def get_response(openai_api, request):
    """
    Get a response from the OpenAI API.

    Args:
        openai (OpenAI): The OpenAI instance.
        request (dict): The request for the OpenAI API.

    Returns:
        str: The content of the response.
    """
    completion = openai_api.ChatCompletion.create(**request)
    if 'content' in completion['choices'][0]['message']:
        review = completion['choices'][0]['message']['content']
        return review
    else:
        raise ValueError("Missing content in response.")

def setup_openai_api():
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError('Missing OpenAI API Key.')
    else:
        openai.api_key = api_key

def load_code_from_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except (FileNotFoundError, PermissionError) as e:
        print(f"Cannot open file {file_path}: {str(e)}")
        raise

def main():
    if len(sys.argv) < 2:
        print('Please provide a file path.')
        sys.exit(1)

    setup_openai_api()

    code = load_code_from_file(sys.argv[1])
    prompt = (f"Tinjau kode di bawah ini"
              f"dan berikan umpan balik tentang cara memperbaikinya.\n{code}")

    response = get_response(openai, {
        "model": "gpt-4",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    })

    print(f"{Fore.BLUE}Review {sys.argv[1]}:{Fore.GREEN}\n{response}{Style.RESET_ALL}\n")

if __name__ == "__main__":
   main()