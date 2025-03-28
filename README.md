# HOSPITAL Management REST API

This is  a RESTful API that manage hospital operations involving Doctors, Assistants, Patients, and Treatments. 
### Technologies Used

FastAPI – backend framework for building APIs quickly and efficiently

SQLAlchemy – ORM for interacting with the database

Alembic – tool for managing database schema migrations

PyJWT – handles JWT authentication

Microsoft SQL Server – relational database used for this project

### Project structure

- `app/` 
  - `models/` – SQLAlchemy models
  - `schemas/` – Pydantic schemas for request/response validation
  - `crud/` – Operations
  - `api/` – Route registrations
  - `auth/` – Authentication and token logic
  - `database/` - DB session configuration and SQLAlchemy Base model import
- `migrations/` – Alembic migrations
- `main.py` – Script for loading sample data
- `load_fixture.py` – App entry point
- `tests` - Tests for operations
- `alembic.ini` - Alembic DB migration configuration
- `pytest.ini` - Pytest config
- `requirements.txt` - Used for installing dependencies

### Development process

1. SQLAlchemy models were created for each entity.
2. Each role has separate routes, protected by JWT and `Depends(role_checker)`.
3. While creating the project, I used Postman to send requests to the application to verify all operations.
4. For testing, I created the tests file containing various tests.
5. For popularization, I created the `load_fixture.py` script.

## Installation Instructions

### Create and activate virtual environment

python -m venv .venv

source .venv/Scripts/activate

### Install dependencies

pip install -r requirements.txt

## Database Setup

Run Alembic migration: alembic upgrade head 

Load sample data: python load_fixture.py

## Runing the application

uvicorn app.main:app --reload

## Authentication

-uses JWT tokens, and for obtain one:

POST /login

Request body:

{
  "username": "manager1",

  "password": "pass"
}


## Roles and Acces Control

Manager: Full CRUD on all entities, reports, user management

Doctor: Can manage their own patients

Assistant: Can only apply treatments to assigned patients

## API Endpoints

| Endpoint                      | Method | Role(s)         | Description                                           |
|------------------------------|--------|------------------|-------------------------------------------------------|
| `/login`                     | POST   | all              | Authenticates user and returns JWT                    |
| `/users/`                    | GET    | manager          | List all users                                        |
| `/users/`                    | POST   | manager          | Create new user                                       |
| `/doctors/`                  | CRUD   | manager          | Manage doctors                                        |
| `/assistants/`               | CRUD   | manager          | Manage assistants                                     |
| `/patients/`                 | POST   | manager, doctor  | Create new patient                                    |
| `/patients/my`              | GET    | doctor           | Doctor’s patients only                                |
| `/patients/`                 | GET    | manager          | All patients                                          |
| `/assignments/`              | CRUD   | manager, doctor  | Assign assistant to patient                           |
| `/treatments/`               | CRUD   | manager, doctor  | Manage treatments                                     |
| `/applications/my`           | GET    | assistant        | View treatments applied by current assistant          |
| `/report/doctors-report`     | GET    | manager          | JSON report: doctors with their patients              |
| `/report/patient-treatments/{id}` | GET | doctor, manager | JSON report: treatments applied to patient            |

## Testing

Tests are provided using pytest and mockups.

To run tests: pytest tests/

## Potential Vulnerabilities

**Weak password storage**: Passwords are hashed with bcrypt (safe), but no password policy applied.

**Hardcoded secret key**: WT SECRET_KEY is currently hardcoded in code.

**No rate limiting**: Login endpoint can be brute-forced if not protected externally.

**No HTTPS enforced**: If deployed in production, token theft via HTTP is possible.



