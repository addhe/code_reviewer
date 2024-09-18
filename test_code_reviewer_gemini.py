import unittest
import os
import io
import sys
from unittest.mock import patch, MagicMock
from colorama import Fore, Style
import google.generativeai as genai
from code_reviewer_gemini import get_response, setup_gemini_api, load_code_from_file, review_code, main


class CodeReviewerTest(unittest.TestCase):

    @patch.dict(os.environ, {"GOOGLE_GEMINI_API_KEY": "test_api_key"})
    def test_setup_gemini_api(self):
        """Test that setup_gemini_api configures the API with the key."""
        # No direct way to verify API key setting in google.generativeai
        # Assuming successful configuration if no exception is raised
        setup_gemini_api()

    def test_setup_gemini_api_missing_key(self):
        """Test that setup_gemini_api raises ValueError if key is missing."""
        with self.assertRaises(ValueError) as context:
            with patch.dict(os.environ, {}, clear=True):
                setup_gemini_api()
        self.assertEqual(str(context.exception),
                         "Missing GOOGLE GEMINI API Key.")

    def test_get_response_valid(self):
        """Test get_response with a valid response."""
        mock_chat = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "Test response"
        mock_chat.send_message.return_value = mock_response
        response = get_response(mock_chat, "Test prompt")
        self.assertEqual(response, "Test response")

    def test_get_response_missing_content(self):
        """Test get_response raises ValueError if response is missing content."""
        mock_chat = MagicMock()
        mock_chat.send_message.return_value = None
        with self.assertRaises(ValueError) as context:
            get_response(mock_chat, "Test prompt")
        self.assertEqual(str(context.exception),
                         "Missing content in response.")

    def test_load_code_from_file_valid(self):
        """Test load_code_from_file with a valid file."""
        file_path = "test.sql"
        with open(file_path, "w", encoding="utf-8") as file:
            file.write("SELECT * FROM test_table;")

        code = load_code_from_file(file_path)

        self.assertEqual(code, "SELECT * FROM test_table;")
        os.remove(file_path)  # Clean up the test file

    def load_code_from_file(file_path):
        """Test load_code_from_file raises FileNotFoundError if file not found."""
        file_path = "./nonexistent.sql"
        with self.assertRaises(FileNotFoundError):  # No need for 'as context'
            load_code_from_file(file_path)

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
        except FileNotFoundError as e:
            print(f"Cannot open file {file_path}: {str(e)}")
            raise e
        except PermissionError as e:
            print(f"Cannot open file {file_path}: {str(e)}")
            raise e

    @patch("code_reviewer_gemini.genai.GenerativeModel")
    def test_review_code_success(self, mock_model):
        """Test review_code with a successful response."""
        mock_chat = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "Review of the code."
        mock_chat.send_message.return_value = mock_response
        mock_model.return_value.start_chat.return_value = mock_chat
        response = review_code("Test prompt", "Test code")
        self.assertEqual(response, "Review of the code.")

    @patch("code_reviewer_gemini.genai.GenerativeModel")
    def test_review_code_error(self, mock_model):
        """Test review_code with an error during processing."""
        mock_chat = MagicMock()
        mock_chat.send_message.side_effect = Exception("Test error")
        mock_model.return_value.start_chat.return_value = mock_chat
        response = review_code("Test prompt", "Test code")
        self.assertTrue("Error: Test error" in response)

    @patch("code_reviewer_gemini.get_response", return_value="Review of the code.")
    @patch("code_reviewer_gemini.load_code_from_file", return_value="Test code")
    @patch("code_reviewer_gemini.setup_gemini_api")
    @patch.object(sys, 'argv', ["code_reviewer_gemini.py", "Test prompt", "test.sql"])
    def test_main_success(self, mock_setup, mock_load_code, mock_get_response):
        """Test main function with successful code review."""
        with patch("sys.stdout", new_callable=io.StringIO) as stdout:
            main()
            output = stdout.getvalue()
            expected_output = (
                f"{Fore.BLUE}Review test.sql:{Fore.GREEN}\n"
                f"Review of the code.{Style.RESET_ALL}\n"
            )
            self.assertIn(expected_output, output)

    @patch.object(sys, 'argv', ["code_reviewer_gemini.py"])
    def test_main_missing_arguments(self):
        """Test main function with missing arguments."""
        with patch("sys.stdout", new_callable=io.StringIO) as stdout:  # Capture stdout
            with self.assertRaises(SystemExit) as cm:
                main()
            self.assertEqual(cm.exception.code, 1)
            self.assertIn(
                "Please provide a prompt and a file path.", stdout.getvalue()
            )
