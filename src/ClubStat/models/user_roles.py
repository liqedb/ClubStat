from dataclasses import dataclass

@dataclass(slots=True)
class UserRole:
    user_role_id: int
    name: str
