from database import dataclass

@dataclass
class Coach_workout:
    coach_workout_id: int
    coach_id: int
    workout_id: int