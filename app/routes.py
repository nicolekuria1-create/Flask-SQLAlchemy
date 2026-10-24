from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from .extensions import db
from .models import Exercise, Workout, WorkoutExercise
from .schemas import (
    ExerciseCreateSchema,
    ExerciseSchema,
    WorkoutCreateSchema,
    WorkoutExerciseCreateSchema,
    WorkoutExerciseSchema,
    WorkoutSchema,
)

api_bp = Blueprint("api", __name__)

workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)
exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)
workout_exercise_schema = WorkoutExerciseSchema()
workout_create_schema = WorkoutCreateSchema()
exercise_create_schema = ExerciseCreateSchema()
workout_exercise_create_schema = WorkoutExerciseCreateSchema()


@api_bp.errorhandler(ValidationError)
def handle_validation_error(err):
    return jsonify({"errors": err.messages}), 400


@api_bp.get("/workouts")
def list_workouts():
    workouts = Workout.query.order_by(Workout.workout_date.desc()).all()
    return jsonify(workouts_schema.dump(workouts)), 200


@api_bp.post("/workouts")
def create_workout():
    payload = workout_create_schema.load(request.get_json() or {})
    workout = Workout(**payload)
    db.session.add(workout)
    db.session.commit()
    return jsonify(workout_schema.dump(workout)), 201


@api_bp.get("/workouts/<int:workout_id>")
def get_workout(workout_id):
    workout = Workout.query.get_or_404(workout_id)
    return jsonify(workout_schema.dump(workout)), 200


@api_bp.delete("/workouts/<int:workout_id>")
def delete_workout(workout_id):
    workout = Workout.query.get_or_404(workout_id)
    db.session.delete(workout)
    db.session.commit()
    return jsonify({"message": f"Workout {workout_id} deleted"}), 200


@api_bp.get("/exercises")
def list_exercises():
    exercises = Exercise.query.order_by(Exercise.name.asc()).all()
    return jsonify(exercises_schema.dump(exercises)), 200


@api_bp.post("/exercises")
def create_exercise():
    payload = exercise_create_schema.load(request.get_json() or {})
    exercise = Exercise(**payload)
    db.session.add(exercise)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "exercise name must be unique"}), 409
    return jsonify(exercise_schema.dump(exercise)), 201


@api_bp.get("/exercises/<int:exercise_id>")
def get_exercise(exercise_id):
    exercise = Exercise.query.get_or_404(exercise_id)
    return jsonify(exercise_schema.dump(exercise)), 200


@api_bp.delete("/exercises/<int:exercise_id>")
def delete_exercise(exercise_id):
    exercise = Exercise.query.get_or_404(exercise_id)
    db.session.delete(exercise)
    db.session.commit()
    return jsonify({"message": f"Exercise {exercise_id} deleted"}), 200


@api_bp.post("/workouts/<int:workout_id>/exercises")
def add_exercise_to_workout(workout_id):
    workout = Workout.query.get_or_404(workout_id)
    payload = workout_exercise_create_schema.load(request.get_json() or {})

    exercise = Exercise.query.get(payload["exercise_id"])
    if not exercise:
        return jsonify({"error": "exercise_id not found"}), 404

    workout_exercise = WorkoutExercise(workout=workout, **payload)
    db.session.add(workout_exercise)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "exercise already added to this workout"}), 409

    return jsonify(workout_exercise_schema.dump(workout_exercise)), 201
