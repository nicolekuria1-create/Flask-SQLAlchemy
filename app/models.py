from datetime import date

from sqlalchemy import CheckConstraint
from sqlalchemy.orm import validates

from .extensions import db


class WorkoutExercise(db.Model):
    __tablename__ = "workout_exercises"

    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey("workouts.id", ondelete="CASCADE"), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey("exercises.id", ondelete="CASCADE"), nullable=False)
    sets = db.Column(db.Integer, nullable=False)
    reps = db.Column(db.Integer, nullable=True)
    duration_seconds = db.Column(db.Integer, nullable=True)
    notes = db.Column(db.String(255), nullable=True)

    workout = db.relationship("Workout", back_populates="workout_exercises")
    exercise = db.relationship("Exercise", back_populates="exercise_workouts")

    __table_args__ = (
        db.UniqueConstraint("workout_id", "exercise_id", name="uq_workout_exercise_pair"),
        CheckConstraint("sets > 0", name="ck_sets_positive"),
        CheckConstraint("reps IS NULL OR reps > 0", name="ck_reps_positive"),
        CheckConstraint(
            "duration_seconds IS NULL OR duration_seconds > 0",
            name="ck_duration_positive",
        ),
        CheckConstraint(
            "NOT (reps IS NULL AND duration_seconds IS NULL)",
            name="ck_reps_or_duration_required",
        ),
    )

    @validates("sets")
    def validate_sets(self, key, value):
        if value is None or value <= 0:
            raise ValueError("sets must be greater than 0")
        return value

    @validates("reps")
    def validate_reps(self, key, value):
        if value is not None and value <= 0:
            raise ValueError("reps must be greater than 0 when provided")
        return value

    @validates("duration_seconds")
    def validate_duration(self, key, value):
        if value is not None and value <= 0:
            raise ValueError("duration_seconds must be greater than 0 when provided")
        return value


class Workout(db.Model):
    __tablename__ = "workouts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    workout_date = db.Column(db.Date, nullable=False, default=date.today)
    trainer_name = db.Column(db.String(120), nullable=False)

    workout_exercises = db.relationship(
        "WorkoutExercise",
        back_populates="workout",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    __table_args__ = (
        CheckConstraint("LENGTH(title) >= 3", name="ck_workout_title_min_len"),
        CheckConstraint("LENGTH(trainer_name) >= 2", name="ck_trainer_name_min_len"),
    )

    @validates("title")
    def validate_title(self, key, value):
        if not value or len(value.strip()) < 3:
            raise ValueError("title must be at least 3 characters")
        return value.strip()

    @validates("trainer_name")
    def validate_trainer_name(self, key, value):
        if not value or len(value.strip()) < 2:
            raise ValueError("trainer_name must be at least 2 characters")
        return value.strip()


class Exercise(db.Model):
    __tablename__ = "exercises"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)
    category = db.Column(db.String(80), nullable=False)
    equipment = db.Column(db.String(80), nullable=True)

    exercise_workouts = db.relationship(
        "WorkoutExercise",
        back_populates="exercise",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    __table_args__ = (
        CheckConstraint("LENGTH(name) >= 2", name="ck_exercise_name_min_len"),
        CheckConstraint("LENGTH(category) >= 3", name="ck_exercise_category_min_len"),
    )

    @validates("name")
    def validate_name(self, key, value):
        if not value or len(value.strip()) < 2:
            raise ValueError("name must be at least 2 characters")
        return value.strip().title()

    @validates("category")
    def validate_category(self, key, value):
        if not value or len(value.strip()) < 3:
            raise ValueError("category must be at least 3 characters")
        return value.strip().title()
