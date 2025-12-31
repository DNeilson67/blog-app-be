# Blog API Backend

A FastAPI-based RESTful API for a blog application with user authentication, posts, and comments.

## Features

- **User Authentication**: JWT-based authentication with bcrypt password hashing
- **Post Management**: Full CRUD operations for blog posts
- **Comment Management**: Full CRUD operations for comments
- **Authorization**: Role-based access control (only authors can edit/delete their content)
- **API Documentation**: Automatic Swagger/OpenAPI documentation
- **PostgreSQL Database**: Using SQLAlchemy ORM

## Setup

### Prerequisites

- Python 3.8+
- PostgreSQL database

### Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment variables:
   - Copy `.env.example` to `.env`
   - Update the `DATABASE_URL` with your PostgreSQL credentials
   - Update the `SECRET_KEY` for JWT token generation

3. Run the application:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, access the interactive API documentation at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Authentication
- `POST /auth/register` - Register a new user
- `POST /auth/login` - Login with email and password
- `POST /auth/logout` - Logout (client-side token invalidation)

### Posts
- `POST /posts` - Create a new post (authenticated)
- `GET /posts` - Get all posts
- `GET /posts/{id}` - Get a specific post by ID
- `PUT /posts/{id}` - Update a post (author only)
- `DELETE /posts/{id}` - Delete a post (author only)

### Comments
- `POST /posts/{id}/comments` - Add a comment to a post (authenticated)
- `GET /posts/{id}/comments` - Get all comments for a post
- `PUT /comments/{id}` - Update a comment (author only)
- `DELETE /comments/{id}` - Delete a comment (author only)

### Users
- `GET /users/me` - Get current user profile (authenticated)
- `PUT /users/me` - Update current user profile (authenticated)
- `GET /users/me/posts` - Get all posts by current user (authenticated)

## Database Schema

### Users
- `id` (String, Primary Key)
- `email` (String, Unique)
- `password` (String, Hashed)
- `name` (String)
- `profile_picture` (String, Optional)
- `created_at` (DateTime)

### Posts
- `id` (String, Primary Key)
- `title` (String)
- `content` (Text)
- `excerpt` (String, Optional)
- `category` (String, Optional)
- `author_id` (String, Foreign Key)
- `created_at` (DateTime)
- `updated_at` (DateTime)

### Comments
- `id` (String, Primary Key)
- `content` (Text)
- `post_id` (String, Foreign Key)
- `author_id` (String, Foreign Key)
- `created_at` (DateTime)
- `updated_at` (DateTime)

## Error Handling

The API returns appropriate HTTP status codes and error messages:
- `400 Bad Request` - Invalid request data
- `401 Unauthorized` - Invalid or missing authentication
- `403 Forbidden` - Insufficient permissions
- `404 Not Found` - Resource not found
- `422 Unprocessable Entity` - Validation error
- `500 Internal Server Error` - Server error

## Security

- Passwords are hashed using bcrypt
- JWT tokens for authentication
- Authorization checks for edit/delete operations
- CORS configured for frontend integration
