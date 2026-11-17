from __future__ import annotations

from ..database import get_connection
from ..models import Coach, CoachWorkout, Reservation, User, Workout

class UserRepository:
    def get_by_id(self, user_id: int) -> User | None:
        with get_connection() as c:
            r = c.execute("SELECT * FROM users WHERE user_id=?", (user_id,)).fetchone()
        return User(**dict(r)) if r else None

    def get_by_login(self, login: str) -> User | None:
        with get_connection() as c:
            r = c.execute("SELECT * FROM users WHERE login=?", (login,)).fetchone()
        return User(**dict(r)) if r else None

    def create(self, name: str, surname: str, patronymic: str | None, login: str, password_hash: str, role: int = 2) -> int:
        with get_connection() as c:
            cur = c.execute("INSERT INTO users(name,surname,patronymic,login,password_hash,user_role) VALUES(?,?,?,?,?,?)",
                            (name, surname, patronymic, login, password_hash, role))
            return int(cur.lastrowid)

    def get_all(self) -> list[User]:
        with get_connection() as c:
            rows = c.execute("SELECT * FROM users ORDER BY surname,name").fetchall()
        return [User(**dict(r)) for r in rows]

class CoachRepository:
    def get_all(self) -> list[Coach]:
        with get_connection() as c:
            rows = c.execute("SELECT * FROM coach ORDER BY surname,name").fetchall()
        return [Coach(**dict(r)) for r in rows]

    def get_by_id(self, coach_id: int) -> Coach | None:
        with get_connection() as c:
            r = c.execute("SELECT * FROM coach WHERE coach_id=?", (coach_id,)).fetchone()
        return Coach(**dict(r)) if r else None

    def create(self, name: str, surname: str, patronymic: str | None = None) -> int:
        with get_connection() as c:
            cur = c.execute("INSERT INTO coach(name,surname,patronymic) VALUES(?,?,?)", (name,surname,patronymic))
            return int(cur.lastrowid)

    def update(self, coach_id: int, name: str, surname: str, patronymic: str | None) -> bool:
        with get_connection() as c:
            cur = c.execute("UPDATE coach SET name=?,surname=?,patronymic=? WHERE coach_id=?", (name,surname,patronymic,coach_id))
            return cur.rowcount > 0

    def delete(self, coach_id: int) -> bool:
        with get_connection() as c:
            cur = c.execute("DELETE FROM coach WHERE coach_id=?", (coach_id,))
            return cur.rowcount > 0

class WorkoutRepository:
    def get_all(self) -> list[Workout]:
        with get_connection() as c:
            rows = c.execute("SELECT * FROM workout ORDER BY name").fetchall()
        return [Workout(**dict(r)) for r in rows]

    def get_by_id(self, workout_id: int) -> Workout | None:
        with get_connection() as c:
            r = c.execute("SELECT * FROM workout WHERE workout_id=?", (workout_id,)).fetchone()
        return Workout(**dict(r)) if r else None

    def create(self, name: str, description: str) -> int:
        with get_connection() as c:
            cur = c.execute("INSERT INTO workout(name,description) VALUES(?,?)", (name,description))
            return int(cur.lastrowid)

    def update(self, workout_id: int, name: str, description: str) -> bool:
        with get_connection() as c:
            cur = c.execute("UPDATE workout SET name=?,description=? WHERE workout_id=?", (name,description,workout_id))
            return cur.rowcount > 0

    def delete(self, workout_id: int) -> bool:
        with get_connection() as c:
            cur = c.execute("DELETE FROM workout WHERE workout_id=?", (workout_id,))
            return cur.rowcount > 0

class CoachWorkoutRepository:
    def assign(self, coach_id: int, workout_id: int) -> int:
        with get_connection() as c:
            cur = c.execute("INSERT INTO coach_workout(coach_id,workout_id) VALUES(?,?)", (coach_id,workout_id))
            return int(cur.lastrowid)

    def get_all(self) -> list[CoachWorkout]:
        with get_connection() as c:
            rows = c.execute("SELECT * FROM coach_workout ORDER BY coach_id").fetchall()
        return [CoachWorkout(**dict(r)) for r in rows]

class ReservationRepository:
    def create(self, visitor_id: int, workout_id: int, reservation_date: str) -> int:
        with get_connection() as c:
            cur = c.execute("INSERT INTO reservation(admin_id,visitor_id,workout_id,reservation_date,status) VALUES(NULL,?,?,?,1)",
                            (visitor_id,workout_id,reservation_date))
            return int(cur.lastrowid)

    def get_for_user(self, visitor_id: int) -> list[dict]:
        with get_connection() as c:
            return [dict(r) for r in c.execute("""SELECT r.*, w.name AS workout_name, s.name AS status_name
                FROM reservation r JOIN workout w USING(workout_id)
                JOIN reservation_status s ON s.reservation_status_id=r.status
                WHERE visitor_id=? ORDER BY reservation_date DESC""", (visitor_id,)).fetchall()]

    def get_all(self) -> list[dict]:
        with get_connection() as c:
            return [dict(r) for r in c.execute("""SELECT r.*, w.name AS workout_name, s.name AS status_name,
                u.login AS visitor_login FROM reservation r JOIN workout w USING(workout_id)
                JOIN reservation_status s ON s.reservation_status_id=r.status
                JOIN users u ON u.user_id=r.visitor_id ORDER BY reservation_date DESC""").fetchall()]

    def cancel(self, reservation_id: int, visitor_id: int | None = None) -> bool:
        sql = "UPDATE reservation SET status=2 WHERE reservation_id=? AND status=1"
        params: tuple = (reservation_id,)
        if visitor_id is not None:
            sql += " AND visitor_id=?"
            params = (reservation_id, visitor_id)
        with get_connection() as c:
            cur = c.execute(sql, params)
            return cur.rowcount > 0
