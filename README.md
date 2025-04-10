# Setting Up the Environment

## Prerequisites
1. Download and install Python 3.10 from the official Python website: [Download Python 3.10](https://www.python.org/downloads/release/python-3100/).

## Steps to Set Up the Environment
1. Create a virtual environment:
    ```bash
    python3.10 -m venv care-env
    ```

2. Activate the virtual environment:
    - On Windows:
      ```bash
      care-env\Scripts\activate
      ```
    - On macOS/Linux:
      ```bash
      source care-env/bin/activate
      ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Run the Flask application:
    ```bash
    python app.py
    ```

## Notes
- Ensure you have a `requirements.txt` file with all necessary dependencies listed.
- If you encounter issues, verify that Python 3.10 is correctly installed and added to your system's PATH.


To contribute Read the CARE pdfs.