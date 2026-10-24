# Workout Tracker API (Flask + SQLAlchemy)

## Project Description
This project is a backend API for a workout tracking application used by personal trainers.
It supports creating and managing workouts, managing reusable exercises, and linking exercises to workouts with sets/reps or duration details.

The API is built with:
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- Marshmallow

## Features
- Create, view, and delete workouts
- Create, view, and delete exercises
- Add an exercise to a workout (many-to-many via association table)
- Database constraints for integrity
- Model-level validation with SQLAlchemy `@validates`
- Schema-level request validation with Marshmallow

## Data Model Overview
- `Workout`
- `Exercise`
- `WorkoutExercise` (association table with metadata: sets, reps, duration_seconds, notes)

Relationship:
- One `Workout` has many `WorkoutExercise` rows
- One `Exercise` has many `WorkoutExercise` rows
- `Workout` and `Exercise` are many-to-many through `WorkoutExercise`

## Installation Instructions
1. Clone the repository.
2. Navigate to the project folder.
3. Install dependencies:

```bash
pipenv install
```

4. Activate the virtual environment:

```bash
pipenv shell
```

## Database Setup (Migrations + Seed)
Run the following commands in order:

```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
python seed.py
```

## Run Instructions
Start the Flask server:

```bash
flask run
```

API base URL:

```text
http://127.0.0.1:5000/api
```

## Endpoints
### Workout Endpoints
- `GET /api/workouts`
  - List all workouts
- `POST /api/workouts`
  - Create a workout
  - Body example:
    ```json
    {
      "title": "Upper Body Power",
      "workout_date": "2026-10-24",
      "trainer_name": "Alex"
    }
    ```
- `GET /api/workouts/<workout_id>`
  - Get one workout with exercise links
- `DELETE /api/workouts/<workout_id>`
  - Delete a workout

### Exercise Endpoints
- `GET /api/exercises`
  - List all exercises
- `POST /api/exercises`
  - Create an exercise
  - Body example:
    ```json
    {
      "name": "Deadlift",
      "category": "Strength",
      "equipment": "Barbell"
    }
    ```
- `GET /api/exercises/<exercise_id>`
  - Get one exercise
- `DELETE /api/exercises/<exercise_id>`
  - Delete an exercise

### Workout-Exercise Endpoint
- `POST /api/workouts/<workout_id>/exercises`
  - Add an exercise to a workout
  - Body example:
    ```json
    {
      "exercise_id": 1,
      "sets": 4,
      "reps": 10,
      "duration_seconds": null,
      "notes": "Slow eccentric"
    }
    ```

## Validations Implemented
### Table Constraints
- Unique exercise name
- Unique `(workout_id, exercise_id)` pair in association table
- Positive checks for sets/reps/duration
- Minimum length checks for key string fields
- Constraint requiring reps or duration to be present in association rows

### Model Validations
- Workout title minimum length
- Trainer name minimum length
- Exercise name and category minimum length
- Positive value validation for sets/reps/duration

### Schema Validations
- Request payload required fields
- Minimum string lengths for names and titles
- Positive integer checks for sets/reps/duration
- Cross-field validation requiring reps or duration

## Seed File
`seed.py` creates starter data for:
- Exercises
- Workouts
- WorkoutExercise associations

## Optional Test Ideas
- Endpoint status code tests with Flask test client
- Validation failure tests (bad payloads)
- Duplicate association and unique exercise name conflict tests

## Author
Your Name
