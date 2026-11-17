"""Create the first administrator account interactively.

Run from the repository root:
    python -m src.ClubStat.admin_setup
"""
import getpass

from .database.init_db import init_db
from .repositories import UserRepository
from .services import AuthService


def main():
    init_db()
    users = UserRepository()
    if any(user.is_admin for user in users.get_all()):
        print("Администратор уже существует.")
        return
    name = input("Имя администратора: ").strip()
    surname = input("Фамилия администратора: ").strip()
    login = input("Логин администратора: ").strip()
    password = getpass.getpass("Пароль (не менее 6 символов): ")
    if users.get_by_login(login):
        print("Этот логин уже занят.")
        return
    if not name or not surname or len(password) < 6:
        print("Проверьте имя, фамилию и длину пароля.")
        return
    users.create(name, surname, None, login, AuthService._hash(password), 1)
    print("Администратор успешно создан.")


if __name__ == "__main__":
    main()
