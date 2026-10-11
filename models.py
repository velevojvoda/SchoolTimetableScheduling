from dataclasses import dataclass
import random

START_MINUTES = 7 * 60
END_MINUTES = 19 * 60
MIN_GAP = 15
TIME_STEP = 15
DAYS = ["Ponedeljak", "Utorak", "Sreda", "Cetvrtak", "Petak"]


@dataclass(frozen=True)
class Event:
    id: int
    name: str
    duration: int  # sve u minutama


@dataclass
class ScheduledEvent:
    event: Event
    day: int
    room_index: int
    start: int

    @property
    def end(self) -> int:
        return self.start + self.event.duration