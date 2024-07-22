# Automated-Job-Search-Analyzer
An automated job search and analysis tool using Python, Selenium, BeautifulSoup, and OpenAI's GPT-4 model to find and evaluate job postings based on user qualifications.

## Installation

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/gilbertijoma/Automated-Job-Search-Analyzer.git
    ```

2. **Install Dependencies**:
    Ensure you have Python installed. Then, install the required packages:
    ```bash
    pip install
    ```

3. **Set Up OpenAI API Key**:
    Replace `'open AI API key'` in the script with your actual OpenAI API key:
    ```python
    openai.api_key = 'open AI API key'
    ```

4. **Prepare Cookies File**:
    Save your authenticated cookies from glassdoor.com in `cookies.json` file in the following format:
    ```json
    [
        {
            "name": "cookie_name",
            "value": "cookie_value",
            "domain": ".glassdoor.com",
            "path": "/",
            "secure": true,
            "httpOnly": true,
            "sameSite": "None"
        }
    ]
    ```

## Usage

1. **Configure Search Parameters**:
    Modify the following variables in the script to match your search criteria:
    ```python
    qualification_criteria = """
    Tech industry job related mostly to software, requires at most a bachelors degree, requires less than two years of work experience, and no government clearance required.
    """
    search_keywords = "Entry level software engineer"
    date_option = 3  # Last week
    remote_only = False  # Set to True for remote jobs only
    ```

2. **Run the Script**:
    Execute the script to start the job search and analysis process:
    ```bash
    python glassdoor.py
    ```
