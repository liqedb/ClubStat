from __future__ import annotations

import hashlib
import hmac
import os
from datetime import datetime

from ..repositories import UserRepository, CoachRepository, WorkoutRepository, ReservationRepository

class AuthService:
    def __init__(self):
        self.users = UserRepository()

    @staticmethod
    def _hash(password: str, salt: bytes | None = None) -> str:
        salt = salt or os.urandom(16)
        digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 180_000)
        return salt.hex() + "$" + digest.hex()

    @staticmethod
    def _verify(password: str, encoded: str) -> bool:
        try:
            salt_hex, digest_hex = encoded.split("$", 1)
            expected = hashlib.pbkdf2_hmac("sha256", password.encode(), bytes.fromhex(salt_hex), 180_000).hex()
            return hmac.compare_digest(expected, digest_hex)
        except (ValueError, TypeError):
            return False

    def register(self, name: str, surname: str, patronymic: str | None, login: str, password: str) -> int:
        if not all(x.strip() for x in (name, surname, login, password)):
            raise ValueError("Заполните имя, фамилию, логин и пароль.")
        if len(password) < 6:
            raise ValueError("Пароль должен содержать не менее 6 символов.")
        if self.users.get_by_login(login.strip()):
            raise ValueError("Такой логин уже зарегистрирован.")
        return self.users.create(name.strip(), surname.strip(), patronymic.strip() if patronymic else None,
                                 login.strip(), self._hash(password), 2)

    def authenticate(self, login: str, password: str):
        user = self.users.get_by_login(login.strip())
        if not user or not self._verify(password, user.password_hash):
            return None
        return user

class ClubService:
    def __init__(self):
        self.coaches = CoachRepository()
        self.workouts = WorkoutRepository()
        self.reservations = ReservationRepository()
        self.users = UserRepository()

    def add_coach(self, name, surname, patronymic=None):
        if not name.strip() or not surname.strip():
            raise ValueError("Имя и фамилия тренера обязательны.")
        return self.coaches.create(name.strip(), surname.strip(), patronymic)

    def add_workout(self, name, description):
        if not name.strip() or not description.strip():
            raise ValueError("Название и описание занятия обязательны.")
        return self.workouts.create(name.strip(), description.strip())

    def book(self, user, workout_id: int, when: str):
        if user.is_admin:
            raise ValueError("Администратор не может записываться как клиент.")
        if not self.workouts.get_by_id(workout_id):
            raise ValueError("Занятие не найдено.")
        try:
            datetime.fromisoformat(when)
        except ValueError:
            raise ValueError("Дата должна быть в формате ГГГГ-ММ-ДД ЧЧ:ММ.")
        return self.reservations.create(user.user_id, workout_id, when)

    def cancel(self, user, reservation_id: int):
        changed = self.reservations.cancel(reservation_id, None if user.is_admin else user.user_id)
        if not changed:
            raise ValueError("Запись не найдена или уже отменена.")
