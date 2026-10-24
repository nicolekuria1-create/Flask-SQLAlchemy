from marshmallow import Schema, ValidationError, fields, validates, validates_schema


class ExerciseCreateSchema(Schema):
    name = fields.Str(required=True)
    category = fields.Str(required=True)
    equipment = fields.Str(load_default=None, allow_none=True)

    @validates("name")
    def validate_name(self, value, **kwargs):
        if len(value.strip()) < 2:
            raise ValidationError("name must be at least 2 characters")

    @validates("category")
    def validate_category(self, value, **kwargs):
        if len(value.strip()) < 3:
            raise ValidationError("category must be at least 3 characters")


class ExerciseSchema(ExerciseCreateSchema):
    id = fields.Int(dump_only=True)


class WorkoutCreateSchema(Schema):
    title = fields.Str(required=True)
    workout_date = fields.Date(required=True)
    trainer_name = fields.Str(required=True)

    @validates("title")
    def validate_title(self, value, **kwargs):
        if len(value.strip()) < 3:
            raise ValidationError("title must be at least 3 characters")

    @validates("trainer_name")
    def validate_trainer_name(self, value, **kwargs):
        if len(value.strip()) < 2:
            raise ValidationError("trainer_name must be at least 2 characters")


class WorkoutExerciseCreateSchema(Schema):
    exercise_id = fields.Int(required=True)
    sets = fields.Int(required=True)
    reps = fields.Int(load_default=None, allow_none=True)
    duration_seconds = fields.Int(load_default=None, allow_none=True)
    notes = fields.Str(load_default=None, allow_none=True)

    @validates("sets")
    def validate_sets(self, value, **kwargs):
        if value <= 0:
            raise ValidationError("sets must be greater than 0")

    @validates("reps")
    def validate_reps(self, value, **kwargs):
        if value is not None and value <= 0:
            raise ValidationError("reps must be greater than 0 when provided")

    @validates("duration_seconds")
    def validate_duration(self, value, **kwargs):
        if value is not None and value <= 0:
            raise ValidationError("duration_seconds must be greater than 0 when provided")

    @validates_schema
    def validate_rep_or_duration(self, data, **kwargs):
        if data.get("reps") is None and data.get("duration_seconds") is None:
            raise ValidationError("Provide reps or duration_seconds")


class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    workout_id = fields.Int(dump_only=True)
    exercise_id = fields.Int(required=True)
    sets = fields.Int(required=True)
    reps = fields.Int(allow_none=True)
    duration_seconds = fields.Int(allow_none=True)
    notes = fields.Str(allow_none=True)
    exercise = fields.Nested(ExerciseSchema, dump_only=True)


class WorkoutSchema(WorkoutCreateSchema):
    id = fields.Int(dump_only=True)
    workout_exercises = fields.List(fields.Nested(WorkoutExerciseSchema), dump_only=True)
