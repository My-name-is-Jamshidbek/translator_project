# Translator Project

This is a Django-based web application for translating words or phrases between literary Uzbek and the Khorezm dialect. The project provides a user-friendly interface for inputting text and selecting the translation direction.

## Features

- Translate between literary Uzbek and the Khorezm dialect.
- User-friendly web interface with Bootstrap styling.
- Text-to-speech functionality for input and output text.
- Responsive design for desktop and mobile devices.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/My-name-is-Jamshidbek/translator_project.git
   cd translator_project
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r req.txt
   ```

4. Run database migrations:
   ```bash
   python manage.py migrate
   ```

5. Start the development server:
   ```bash
   python manage.py runserver
   ```

6. Open the application in your browser:
   ```
   http://127.0.0.1:8000/
   ```

## Usage

1. Enter a word or phrase in the input field.
2. Select the translation direction:
   - Literary Uzbek → Khorezm dialect
   - Khorezm dialect → Literary Uzbek
3. Click the "Yuborish" button to get the translation.
4. View the results and the Khorezm dialect form of the input text.

## Dependencies

- Python 3.x
- Django
- Bootstrap 4.5.2
- jQuery 3.5.1

## Project Structure

- `translator_app/`: Contains the main application logic.
- `templates/`: HTML templates for the web interface.
- `static/`: Static files such as CSS and JavaScript.
- `requirements.txt`: List of Python dependencies.

## GitHub Repository

[Translator Project](https://github.com/My-name-is-Jamshidbek/translator_project.git)