from database import dataclass

@dataclass
class Users:
    user_id: int
    name: str
    surname: str
    patronymic: str | None = None
    login: str
    password: str
    user_role: int