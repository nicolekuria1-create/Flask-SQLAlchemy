from datetime import date

from app import create_app
from app.extensions import db
from app.models import Exercise, Workout, WorkoutExercise

app = create_app()


with app.app_context():
    print("Clearing old data...")
    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()

    print("Seeding exercises...")
    squat = Exercise(name="Back Squat", category="Strength", equipment="Barbell")
    run = Exercise(name="Treadmill Run", category="Cardio", equipment="Treadmill")
    plank = Exercise(name="Plank", category="Core", equipment=None)
    press = Exercise(name="Shoulder Press", category="Strength", equipment="Dumbbells")

    print("Seeding workouts...")
    workout_1 = Workout(
        title="Leg Day Builder",
        workout_date=date(2026, 10, 20),
        trainer_name="Alex",
    )
    workout_2 = Workout(
        title="Cardio Core Blast",
        workout_date=date(2026, 10, 21),
        trainer_name="Jamie",
    )

    db.session.add_all([squat, run, plank, press, workout_1, workout_2])
    db.session.flush()

    print("Linking exercises to workouts...")
    links = [
        WorkoutExercise(
            workout_id=workout_1.id,
            exercise_id=squat.id,
            sets=5,
            reps=5,
            notes="Focus on depth",
        ),
        WorkoutExercise(
            workout_id=workout_1.id,
            exercise_id=press.id,
            sets=4,
            reps=8,
            notes="Controlled tempo",
        ),
        WorkoutExercise(
            workout_id=workout_2.id,
            exercise_id=run.id,
            sets=1,
            duration_seconds=1800,
            notes="Steady pace",
        ),
        WorkoutExercise(
            workout_id=workout_2.id,
            exercise_id=plank.id,
            sets=3,
            duration_seconds=60,
            notes="Tight core",
        ),
    ]

    db.session.add_all(links)
    db.session.commit()
    print("Done seeding database.")
