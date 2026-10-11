
# Bakery Website

A responsive bakery website built with Flask and MySQL. Customers can view the website and submit order requests through a form. An administrator can log in to manage incoming requests.

## Features

- Responsive website interface
- Customer order request form
- Form validation for required fields and phone numbers
- MySQL database for storing order requests
- Administrator login and session-based access control
- Admin panel for viewing and deleting requests
- CSRF protection for forms
- Rate limiting for login attempts
- Automated tests with pytest

## Technologies

- Python
- Flask
- MySQL
- SQLAlchemy
- HTML
- CSS
- Flask-WTF
- Flask-Limiter
- pytest

## Project Structure

```text
bakery_website/
├── app.py
├── test_app.py
├── templates/
│   ├── index.html
│   ├── admin.html
│   └── login.html
├── static/
│   └── css/
│       └── style.css
├── .env
└── .gitignore
```

## Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/kamishaga44/bakery_website.git
   cd bakery_website
   ```

2. Create and activate a virtual environment:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```


3. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file with your local database settings, administrator password, and Flask secret key.

5. Create and configure the MySQL database.

6. Run the application:

   ```bash
   python app.py
   ```

## Running Tests

Run the automated tests with:

```bash
pytest -v
```

## Security Notes

- Keep `.env` out of version control.
- Use a strong secret key and administrator password.
- Disable Flask debug mode before deploying the application.
- Configure persistent storage for rate limiting in production.

## Author

Developed as a portfolio project to practice web development with Python, Flask, and MySQL.
