from __future__ import annotations

from .database.init_db import init_db
from .services import AuthService, ClubService
from .repositories import UserRepository

auth = AuthService()
club = ClubService()

def ask_int(prompt: str) -> int:
    return int(input(prompt).strip())

def show_workouts():
    items = club.workouts.get_all()
    if not items:
        print("Занятий пока нет.")
    for x in items:
        print(f"{x.workout_id}. {x.name} — {x.description}")

def admin_menu(user):
    while True:
        print("\n=== CLUBSTAT / АДМИНИСТРАТОР ===")
        print("1. Список занятий  2. Добавить занятие  3. Удалить занятие")
        print("4. Список тренеров 5. Добавить тренера 6. Все бронирования")
        print("7. Отменить бронирование 0. Выход")
        choice = input("> ").strip()
        try:
            if choice == "1": show_workouts()
            elif choice == "2":
                wid = club.add_workout(input("Название: "), input("Описание: "))
                print(f"Занятие добавлено, ID={wid}")
            elif choice == "3":
                wid = ask_int("ID занятия: ")
                if not club.workouts.delete(wid): print("Занятие не найдено.")
                else: print("Занятие удалено.")
            elif choice == "4":
                for c in club.coaches.get_all(): print(f"{c.coach_id}. {c.surname} {c.name} {c.patronymic or ''}")
            elif choice == "5":
                cid = club.add_coach(input("Имя: "), input("Фамилия: "), input("Отчество (необязательно): ") or None)
                print(f"Тренер добавлен, ID={cid}")
            elif choice == "6":
                for r in club.reservations.get_all(): print(f"#{r['reservation_id']} {r['visitor_login']} — {r['workout_name']} — {r['reservation_date']} [{r['status_name']}]")
            elif choice == "7":
                club.cancel(user, ask_int("ID бронирования: "))
                print("Бронирование отменено.")
            elif choice == "0": return
            else: print("Неизвестный пункт меню.")
        except (ValueError, Exception) as exc:
            print(f"Ошибка: {exc}")

def visitor_menu(user):
    while True:
        print("\n=== CLUBSTAT / КЛИЕНТ ===")
        print("1. Расписание  2. Записаться  3. Мои бронирования  4. Отменить запись  0. Выход")
        choice = input("> ").strip()
        try:
            if choice == "1": show_workouts()
            elif choice == "2":
                show_workouts()
                rid = club.book(user, ask_int("ID занятия: "), input("Дата и время (ГГГГ-ММ-ДД ЧЧ:ММ): "))
                print(f"Вы записаны. Номер бронирования: {rid}")
            elif choice == "3":
                for r in club.reservations.get_for_user(user.user_id):
                    print(f"#{r['reservation_id']} {r['workout_name']} — {r['reservation_date']} [{r['status_name']}]")
            elif choice == "4":
                club.cancel(user, ask_int("ID бронирования: "))
                print("Запись отменена.")
            elif choice == "0": return
            else: print("Неизвестный пункт меню.")
        except Exception as exc:
            print(f"Ошибка: {exc}")

def main():
    init_db()
    while True:
        print("\n=== CLUBSTAT ===\n1. Войти\n2. Регистрация\n0. Выход")
        choice = input("> ").strip()
        try:
            if choice == "1":
                user = auth.authenticate(input("Логин: "), input("Пароль: "))
                if not user: print("Неверный логин или пароль.")
                elif user.is_admin: admin_menu(user)
                else: visitor_menu(user)
            elif choice == "2":
                uid = auth.register(input("Имя: "), input("Фамилия: "), input("Отчество: ") or None,
                                    input("Логин: "), input("Пароль: "))
                print(f"Регистрация успешна. Ваш ID: {uid}")
            elif choice == "0": break
            else: print("Неизвестный пункт меню.")
        except Exception as exc:
            print(f"Ошибка: {exc}")

if __name__ == "__main__":
    main()
