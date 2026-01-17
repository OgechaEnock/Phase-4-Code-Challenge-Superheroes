# Superheroes API

A Flask REST API for managing superheroes and their superpowers.

## Author
Enock Ogecha

## Description

This API manages superheroes, their powers, and relationships between them. Built with Flask and SQLAlchemy with data validation and email functionality.

## Technologies Used

- Python 3.8+
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- Flask-Mail
- SQLite

## Installation & Setup
```bash
# Clone repository
git clone (paste repository url)


# Create virtual environment
python3 -m venv venv
source venv/bin/activate 

# Install dependencies
pip install -r requirements.txt

# Set up email
export MAIL_USERNAME="enockogecha7@@gmail.com"
export MAIL_PASSWORD="your-app-password"

# Initialize database
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
python seed.py

# Run application
python app.py
```

API running at `http://localhost:5555`

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/heroes` | Get all heroes |
| GET | `/heroes/:id` | Get hero with powers |
| GET | `/powers` | Get all powers |
| GET | `/powers/:id` | Get specific power |
| PATCH | `/powers/:id` | Update power description |
| POST | `/hero_powers` | Create hero-power association |
| POST | `/send-email` | Send email notification |

## Features

✅ CRUD operations  
✅ Data validation  
✅ Many-to-many relationships  
✅ Email functionality (Flask-Mail)  
✅ Error handling  

## Project Demonstration

### 1. GET /heroes - Retrieve All Heroes
![GET Heroes](screenshots/get-heroes.png)
*Successfully retrieves all heroes with 200 OK status*

### 2. POST /send-email - Email Functionality
![Send Email](screenshots/send-email.png)
*Demonstrates Flask-Mail sending email successfully*
