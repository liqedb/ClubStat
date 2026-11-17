from dataclasses import dataclass

@dataclass(slots=True)
class ReservationStatus:
    reservation_status_id: int
    name: str
