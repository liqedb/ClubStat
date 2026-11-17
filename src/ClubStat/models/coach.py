from dataclasses import dataclass

@dataclass(slots=True)
class Coach:
    coach_id: int
    name: str
    surname: str
    patronymic: str | None = None
