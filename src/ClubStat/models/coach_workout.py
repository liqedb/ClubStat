from dataclasses import dataclass

@dataclass(slots=True)
class CoachWorkout:
    coach_workout_id: int
    coach_id: int
    workout_id: int
