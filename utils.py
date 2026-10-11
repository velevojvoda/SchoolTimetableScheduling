from models import ScheduledEvent, DAYS


def minutes_to_hhmm(m):
    return f"{m // 60:02d}:{m % 60:02d}"


def print_timetable(ind, data):
    schedule = {}

    for g in ind.genes:
        schedule.setdefault((g.room_index, g.day), []).append(g)

    for r_index, room in enumerate(data.rooms):
        print("=" * 60)
        print(f"UČIONICA: {room}")
        print("=" * 60)

        for d in range(len(DAYS)):
            key = (r_index, d)
            if key not in schedule:
                continue

            events = sorted(schedule[key], key=lambda g: g.start)
            print(f"  {DAYS[d]}:")
            for e in events:
                print(f"    {minutes_to_hhmm(e.start)} - {minutes_to_hhmm(e.end)}  |  {e.event.name}")
            print()