from dotenv import load_dotenv
import os
import sys
import openai

# Load environment variables from a .env file
load_dotenv()

# Set color codes
reset = '\x1b[0m'
green = '\x1b[32m'

def get_response(openai, request):
    """
    Get a response from the OpenAI API.

    Args:
        openai (OpenAI): The OpenAI instance.
        request (dict): The request for the OpenAI API.

    Returns:
        str: The content of the response.
    """
    completion = openai.ChatCompletion.create(**request)
    review = completion.choices[0].message['content']
    return review


def main():
    if len(sys.argv) < 2:
        print('Please provide a file path.')
        sys.exit(1)

    file_path = sys.argv[1]

    # Read the file and get the code.
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            code = file.read()
    except (FileNotFoundError, PermissionError) as e:
        print(f"Cannot open file {file_path}: {str(e)}")
        sys.exit(1)

    prompt = f"""
    Tinjau kode di bawah ini dan berikan umpan balik tentang cara memperbaikinya.

    {code}
    """
    

    api_key = os.getenv('OPENAI_API_KEY')

    if not api_key:
        print('Missing OpenAI API Key.')
        sys.exit(1)

    openai.api_key = api_key

    response = get_response(openai, {
        "model": "gpt-4",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    })

    print(f"{green}Review {file_path}:{reset}\n{response}{reset}\n")


if __name__ == "__main__":
   main()