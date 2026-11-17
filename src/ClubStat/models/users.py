from dataclasses import dataclass

@dataclass(slots=True)
class User:
    user_id: int
    name: str
    surname: str
    patronymic: str | None
    login: str
    password_hash: str
    user_role: int

    @property
    def is_admin(self) -> bool:
        return self.user_role == 1
