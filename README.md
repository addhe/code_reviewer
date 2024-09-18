# Code Reviewer with Gemini API

This script leverages the Google Gemini API to provide code reviews based on user-defined prompts. 

## Features

- **Gemini API Integration:**  Uses the Google Gemini API for natural language understanding and code analysis.
- **Custom Prompts:**  Allows users to provide their own prompts for code review, tailoring the analysis to specific needs.
- **Code File Input:**  Accepts a file path to the code that needs to be reviewed.
- **User-Friendly Output:**  Presents the review in a clear and organized format, highlighting the Gemini API's feedback.

## Requirements

- Python 3.7 or higher
- Google Cloud Account (for accessing the Gemini API)
- `google-generativeai` library: `pip install google-generativeai`
- `colorama` library: `pip install colorama`

## Setup

1. **Set Up Google Cloud Account:**
   - Create a Google Cloud project.
   - Enable the Gemini API within your project.
   - Get your API key from the Google Cloud console (you'll need to configure billing for the API).

2. **Environment Variable:**
   - Set the environment variable `GOOGLE_GEMINI_API_KEY` to the key you obtained in step 1.
   - You can do this in your shell: `export GOOGLE_GEMINI_API_KEY="YOUR_API_KEY"`

3. **Install Dependencies:**
   - Install the required libraries using `pip install google-generativeai colorama`.

## Usage

1. **Save the code:** Save the provided Python script as `code_reviewer.py`.
2. **Run the script:** 
   ```bash
   python code_reviewer.py "Your custom prompt here" example.sql
   ```
   - Replace `"Your custom prompt here"` with the prompt you want to use for code review.
   - Replace `example.sql` with the actual file path of the code you want to review.

## Example

```bash
python code_reviewer.py "Please review this SQL query for potential issues and provide suggestions for improvement." my_query.sql
```

## Notes

- **Prompting:**
    - The quality of the code review is highly dependent on the prompt you provide. 
    - Be clear and specific about what you want the Gemini API to focus on.
- **Cost:**  The Gemini API may incur costs for usage. Consult Google Cloud pricing for details.
- **Error Handling:**  The script includes basic error handling, but it may need further enhancement for more robust scenarios.

## Disclaimer

This is a basic implementation of a code reviewer using the Gemini API.  The code review process and the quality of the feedback will depend on the specific capabilities of the Gemini API and the clarity of the user's prompts. 

## License
This code review tool is open-source and distributed under the MIT License. See the LICENSE file for more information.

## Acknowledgements
This code review tool was inspired by the need for a comprehensive and automated solution to review python code at first, now it's more general purpose. Special thanks to the open-source community for their valuable contributions and feedback.