from database import dataclass


@dataclass
class Coach:
    coach_id: int
    name: str
    surname: str
    patronymic: str | None = None