from models import Event


class TimetableData:
    def __init__(self, rooms, events):
        self.rooms = rooms
        self.events = events

    @classmethod
    def from_file(cls, path):
        with open(path, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]

        room_line = lines[0]
        room_part = room_line.split(":", 1)[1]
        rooms = [r.strip() for r in room_part.split(",")]

        events = []
        event_id = 0

        for line in lines[2:]:
            name, dur = line.rsplit(",", 1)
            events.append(Event(id=event_id, name=name.strip(), duration=int(dur)))
            event_id += 1

        return cls(rooms=rooms, events=events)