import requests
import sys


def get_response(prompt: str) -> str:
    """Get a response from the LLaMA model.

    Args:
        prompt (str): The prompt for the LLaMA model.

    Returns:
        str: The content of the response.

    Raises:
        requests.exceptions.RequestException: If there's an error with the request.
    """
    headers = {"Content-Type": "application/json"}
    data = {
        "model": "codegemma",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
    }
    response = requests.post(
        "http://localhost:11434/v1/chat/completions",
        headers=headers,
        json=data
    )
    response.raise_for_status()
    response_json = response.json()

    if ("choices" in response_json and
            len(response_json["choices"]) > 0 and
            "content" in response_json["choices"][0]["message"]):
        return response_json["choices"][0]["message"]["content"]

    raise ValueError("Response does not contain any content.")


def load_code_from_file(file_path: str) -> str:
    """Load code from a file.

    Args:
        file_path (str): The path to the file to load.

    Returns:
        str: The content of the file.

    Raises:
        FileNotFoundError: If the file doesn't exist.
        PermissionError: If the file exists but cannot be read.
        UnicodeDecodeError: If there's an error decoding the file.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except (FileNotFoundError, PermissionError) as e:
        print(f"Error opening file {file_path}: {str(e)}")
        raise
    except UnicodeDecodeError:
        print(f"Error decoding file {file_path}")
        raise


def review_code(prompt: str, code: str) -> str:
    """Review code using the LLaMA model.

    Args:
        prompt (str): The prompt for the LLaMA model.
        code (str): The code to be reviewed.

    Returns:
        str: The review response from the LLaMA model.

    Raises:
        Exception: If there's an error during code review.
    """
    try:
        full_prompt = f"{prompt}\n```\n{code}\n```"
        response = get_response(full_prompt)
        return response
    except Exception as e:
        print(f"Error during code review: {e}")
        return f"Error: {e}"


def main():
    """Command-line interface for code reviewer."""
    if len(sys.argv) < 3:
        print("Please provide a prompt and a file path.")
        sys.exit(1)

    user_prompt = sys.argv[1]
    file_path = sys.argv[2]

    try:
        code = load_code_from_file(file_path)
        response = review_code(user_prompt, code)
        print(f"Review of the code:\n{response}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
