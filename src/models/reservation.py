from database import dataclass

@dataclass
class Reservation:
    reservation_id: int
    admin_id: int
    visitor_id: int
    workout_id: int
    reservation_date: str
    status: int