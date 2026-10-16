from database import dataclass

@dataclass
class Workout:
    workout_id: int
    name: str
    description: str