# Collaborative Code Learning Platform

A real-time collaborative platform for coding education that allows mentors and students to work together on coding exercises.

## Overview

This Flask application provides the backend for a real-time collaborative coding platform. It enables:

- Mentors to create coding exercises with templates and solutions
- Students to join coding rooms and work on exercises
- Real-time code synchronization between participants
- Automatic validation of solutions
- Admin interface for managing coding exercises

## Architecture

### Components

- **Flask Server**: Core web application framework
- **Socket.IO**: Real-time bidirectional communication
- **SQLAlchemy**: ORM for database operations
- **SQLite**: Database storage for code blocks

### Files Structure

- `server.py`: Main application entry point
- `models.py`: Database models and schema definitions
- `api.py`: REST API endpoints for code block management
- `sockets.py`: Socket.IO event handlers for real-time features
- `db_init.py`: Database initialization and sample data loading

## Features

### Code Block Management

- Create, read, update, and delete code exercises
- Each code block includes:
  - Name: Short descriptive title
  - Template: Starting code for students
  - Solution: Correct implementation
  - Explanation: Description of the exercise

### Real-time Collaboration

- Room-based collaboration system
- First user to join a room becomes the mentor
- Subsequent users join as students
- Real-time code synchronization across all participants
- Automatic solution validation

### Room Management

- Active rooms tracking
- Student count updates
- Automatic cleanup when mentors disconnect

## API Endpoints

### Code Block Management

- `GET /api/codeblocks`: List all available code blocks
- `GET /api/codeblocks/<id>`: Get a specific code block (without solution)
- `GET /api/codeblocks/admin`: Get all code blocks with full details
- `POST /api/codeblocks`: Create a new code block
- `PUT /api/codeblocks/<id>`: Update an existing code block
- `DELETE /api/codeblocks/<id>`: Delete a code block

## Socket.IO Events

### Client Events (Incoming)

- `connect`: Client connects to the server
- `join_room`: Client joins a specific code room
- `code_change`: Client sends updated code
- `disconnect`: Client disconnects from the server

### Server Events (Outgoing)

- `active_rooms`: List of active coding rooms
- `role_assignment`: Assigns role (mentor/student) to new participants
- `update_student_count`: Updates count of students in a room
- `update_code`: Sends code updates to all room participants
- `solution_found`: Notifies when solution is correctly implemented
- `solution_incorrect`: Notifies when submitted code is not the solution
- `redirect_to_lobby`: Instructs clients to return to lobby

## Database Schema

### CodeBlock Model

- `id`: Primary key
- `name`: Name of the code exercise
- `template`: Starting code template
- `solution`: Correct implementation
- `explanation`: Description of the exercise

## Setup and Installation

### Prerequisites

- Python 3.7+
- pip

### Installation

1. Clone the repository
```
git clone <repository-url>
cd <repository-directory>
```

2. Create and activate a virtual environment
```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```
pip install flask flask-socketio flask-sqlalchemy flask-cors python-engineio python-socketio
```

4. Run the application
```
python server.py
```

The server will start on `http://localhost:5000` by default.

## Development

### Adding New Code Blocks

You can add new code blocks directly through the API or by modifying the sample data in `db_init.py`.

### Running in Debug Mode

The application runs in debug mode by default, providing detailed error messages and automatic reloading when code changes.

## Project Structure Workflow

1. `server.py` initializes the Flask application and Socket.IO
2. `db_init.py` sets up the database and populates it with sample data
3. `api.py` handles REST endpoints for CRUD operations
4. `sockets.py` manages real-time communication between clients
5. `models.py` defines the database schema

## Client Integration

To connect a client application:

1. Use REST API for code block management
2. Connect to Socket.IO for real-time features
3. Handle the appropriate Socket.IO events as documented above


## Author

Omkiman