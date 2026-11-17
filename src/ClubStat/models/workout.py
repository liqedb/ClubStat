from dataclasses import dataclass

@dataclass(slots=True)
class Workout:
    workout_id: int
    name: str
    description: str
