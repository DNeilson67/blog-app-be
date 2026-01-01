# Blog Application - Backend API

A production-ready FastAPI-based RESTful API for a blog application with comprehensive user authentication, post management, and commenting features. Built with modern Python async patterns, SQLAlchemy ORM, and PostgreSQL.

## Prerequisites

Before running this project, ensure you have:

- **Python** 3.8 or higher
- **PostgreSQL** database server
- **pip** package manager

## Project Setup

### 1. Clone and Navigate

```bash
cd blog-app-be
```

### 2. Create Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the root directory (can be copied from .env.example):

```env
# Database Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/blog_db

# JWT Configuration
SECRET_KEY=your-secret-key-here-generate-with-openssl-rand-hex-32
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS Configuration (optional)
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

### 5. Run the Application

```bash
uvicorn main:app --reload
```

The API will be available at: **http://localhost:8000**

## Project Structure

```
blog-app-be/
├── main.py                       # Application entry point and FastAPI setup
├── requirements.txt              # Python dependencies
├── .env                          # Environment configuration (not in git)
└── src/
    ├── config/
    │   └── settings.py           # Configuration and environment variables
    ├── database/
    │   ├── database.py           # Database connection and session management
    │   ├── models.py             # SQLAlchemy ORM models
    │   └── schemas.py            # Pydantic request/response schemas
    ├── middleware/
    │   ├── auth.py               # Password hashing and JWT utilities
    │   └── dependencies.py       # FastAPI dependency injection
    └── routes/
        ├── auth.py               # Authentication endpoints
        ├── posts.py              # Post management endpoints
        ├── comments.py           # Comment management endpoints
        └── users.py              # User profile endpoints
```

## API Documentation

Once the server is running, access the interactive API documentation:

- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
  - Interactive API testing interface
  - Try out endpoints directly from browser


## Database Schema

### Users Table
| Column | Type | Constraints |
|--------|------|-------------|
| id | String (UUID) | Primary Key |
| email | String | Unique, Not Null |
| password | String (Hashed) | Not Null |
| name | String | Not Null |
| profile_picture | String | Nullable |
| created_at | DateTime | Not Null |

### Posts Table
| Column | Type | Constraints |
|--------|------|-------------|
| id | String (UUID) | Primary Key |
| title | String | Not Null |
| content | Text | Not Null |
| excerpt | String | Nullable |
| category | String | Nullable |
| author_id | String (UUID) | Foreign Key → users.id |
| created_at | DateTime | Not Null |
| updated_at | DateTime | Not Null |

### Comments Table
| Column | Type | Constraints |
|--------|------|-------------|
| id | String (UUID) | Primary Key |
| content | Text | Not Null |
| post_id | String (UUID) | Foreign Key → posts.id |
| author_id | String (UUID) | Foreign Key → users.id |
| created_at | DateTime | Not Null |
| updated_at | DateTime | Not Null |

## How to Interact with the API

1. Start the server: `uvicorn main:app --reload`
2. Navigate to [http://localhost:8000/docs](http://localhost:8000/docs)
3. Register a user via `/auth/register`
4. Login via `/auth/login` to get JWT token, you can use the demo credential below:
```
email: john@example.com
password: password123
```
6. Click "Authorize" button and enter your JWT token.
7. Now you can test all authenticated endpoints

## Design Decisions and Assumptions

This backend uses FastAPI for a modern, high-performance, async API with automatic documentation and built-in validation via Pydantic. Data is stored in PostgreSQL, a reliable and scalable relational database, accessed through SQLAlchemy to provide a secure, database-agnostic ORM layer. Authentication is handled with JWT, enabling stateless and scalable user sessions, while passwords are securely hashed using bcrypt directly for better control and compatibility. UUIDs are used as primary keys to prevent ID-guessing and improve data safety.

The system assumes simple authentication and authorization: tokens expire after 30 minutes, there is no refresh token, email verification, or password reset, and only content authors can edit or delete their own posts. Validation and moderation are minimal, with no pagination, caching, admin roles, or content approval, making it suitable for small to medium datasets. Deployment targets common cloud platforms using environment variables, automatic table creation, and default logging, with limited data integrity features such as no cascade deletes, soft deletes, or audit trails.
