from dataclasses import dataclass

@dataclass(slots=True)
class Reservation:
    reservation_id: int
    admin_id: int | None
    visitor_id: int
    workout_id: int
    reservation_date: str
    status: int
