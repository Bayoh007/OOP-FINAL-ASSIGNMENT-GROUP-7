# Royal Fitness SL API

A FastAPI-based RESTful application for tracking workouts, nutrition, and personal fitness progress. Built as a final group project for **PROG315 - Object-Oriented Programming 2** at Limkokwing University of Creative Technology, Sierra Leone (Semester 4, 2026).

## Project Overview

Royal Fitness SL helps users in Sierra Leone manage their personal fitness journey by logging workouts, tracking nutrition intake, and monitoring progress over time. The application follows industry-standard practices for secure, scalable, and well-documented REST APIs.

## Alignment with Sustainable Development Goals (SDGs)

This project aligns with **SDG 3: Good Health and Well-being**, supporting healthier lifestyles by giving Sierra Leoneans an accessible digital tool to monitor exercise, diet, and personal health goals.

## Features

- **User Management** - Registration, authentication, and profile management
- **Workout Tracking** - Create, view, update, and delete workout sessions (type, duration, intensity, date)
- **Nutrition Logging** - Record meals, calories, and macronutrient intake
- **Progress Monitoring** - Track weight, body measurements, and fitness milestones over time

## Tech Stack

- **Framework:** FastAPI
- **Database:** PostgreSQL with SQLAlchemy ORM
- **Authentication:** OAuth2 + JWT (password hashing for security)
- **Validation:** Pydantic models with Python type annotations
- **Dependency Injection:** FastAPI `Depends()` for database sessions
- **Documentation:** Swagger UI (`/docs`) and ReDoc (`/redoc`)

## Project Structure

```
royal-fitness-sl-api/
├── main.py          # Application entry point and route registration
├── models.py         # SQLAlchemy database models
├── schemas.py         # Pydantic request/response schemas
├── database.py        # Database connection and session setup
├── auth.py           # Authentication and JWT logic
├── .env.example        # Environment variable template (no real credentials)
├── requirements.txt      # Project dependencies
└── README.md
```

## API Endpoints

### Users

|Method|Endpoint         |Description                       |
|------|-----------------|----------------------------------|
|POST  |`/users/register`|Register a new user               |
|POST  |`/users/login`   |Authenticate and receive JWT token|
|GET   |`/users/{id}`    |Get user profile                  |
|PUT   |`/users/{id}`    |Update user profile               |
|DELETE|`/users/{id}`    |Delete user account               |

### Workouts

|Method|Endpoint        |Description                 |
|------|----------------|----------------------------|
|POST  |`/workouts/`    |Log a new workout           |
|GET   |`/workouts/`    |List all workouts for a user|
|GET   |`/workouts/{id}`|Get a specific workout      |
|PUT   |`/workouts/{id}`|Update a workout            |
|DELETE|`/workouts/{id}`|Delete a workout            |

### Nutrition

|Method|Endpoint         |Description                          |
|------|-----------------|-------------------------------------|
|POST  |`/nutrition/`    |Log a meal/nutrition entry           |
|GET   |`/nutrition/`    |List all nutrition entries for a user|
|GET   |`/nutrition/{id}`|Get a specific nutrition entry       |
|PUT   |`/nutrition/{id}`|Update a nutrition entry             |
|DELETE|`/nutrition/{id}`|Delete a nutrition entry             |

### Progress

|Method|Endpoint        |Description                                       |
|------|----------------|--------------------------------------------------|
|POST  |`/progress/`    |Add a progress record (weight, measurements, etc.)|
|GET   |`/progress/`    |List all progress records for a user              |
|GET   |`/progress/{id}`|Get a specific progress record                    |
|PUT   |`/progress/{id}`|Update a progress record                          |
|DELETE|`/progress/{id}`|Delete a progress record                          |

## Getting Started

### Prerequisites

- Python 3.10+
- PostgreSQL installed and running

### Installation

```bash
# Clone the repository
git clone https://github.com/Isata427/royal-fitness-sl-api.git
cd royal-fitness-sl-api

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your database credentials and JWT secret key
```

### Running the Application

```bash
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`

### API Documentation

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Authentication

Most endpoints require a valid JWT token. After registering and logging in via `/users/login`, include the token in the `Authorization` header:

```
Authorization: Bearer <your_token_here>
```

## Contributors

|Name                          |Role     |
|------------------------------|---------|
|Isata Bah                     |Developer|
|*Add other group members here*|         |

## License

This project is licensed under the MIT License - see the <LICENSE> file for details.

## Acknowledgements

- Limkokwing University of Creative Technology, Sierra Leone
- PROG315 - Object-Oriented Programming 2
- Examiner: Amandus Benjamin Coker