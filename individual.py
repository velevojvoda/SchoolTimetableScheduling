import random

from models import (
    Event, ScheduledEvent,
    DAYS, START_MINUTES, END_MINUTES,
    MIN_GAP, TIME_STEP
)
from data_loader import TimetableData


class Individual:
    def __init__(self, data, genes = None):
        self.data = data
        self.genes = genes if genes else self._random_genes()
        self.fitness = None

    def _random_genes(self) :
        genes = []
        num_days = len(DAYS)
        num_rooms = len(self.data.rooms)

        for ev in self.data.events:
            day = random.randint(0, num_days - 1)
            room_index = random.randint(0, num_rooms - 1)

            latest_start = END_MINUTES - ev.duration
            num_slots = (latest_start - START_MINUTES) // TIME_STEP + 1
            slot = random.randint(0, num_slots - 1)
            start = START_MINUTES + slot * TIME_STEP

            genes.append(ScheduledEvent(ev, day, room_index, start))

        return genes

    def clone(self):
        return Individual(
            self.data,
            [
                ScheduledEvent(g.event, g.day, g.room_index, g.start)
                for g in self.genes
            ]
        )

    def _group(self):
        schedule = {}
        for g in self.genes:
            schedule.setdefault((g.room_index, g.day), []).append(g)
        return schedule

    def evaluate_fitness(self):
        if self.fitness is not None:
            return self.fitness

        schedule = self._group()
        penalty = 0
        objective = 0

        for room in range(len(self.data.rooms)):
            for day in range(len(DAYS)):
                key = (room, day)
                if key not in schedule:
                    continue

                events = sorted(schedule[key], key=lambda se: se.start)

                for i, se in enumerate(events):
                    if se.start < START_MINUTES:
                        penalty += START_MINUTES - se.start
                    if se.end > END_MINUTES:
                        penalty += se.end - END_MINUTES

                    if i > 0:
                        gap = se.start - events[i - 1].end
                        if gap < MIN_GAP:
                            penalty += MIN_GAP - gap

                p = events[0].start - START_MINUTES
                k = END_MINUTES - events[-1].end
                objective += max(0, p) * max(0, k)

        self.fitness = objective - 1000 * penalty
        return self.fitness

    def crossover(self, other):
        child_genes = []
        for g1, g2 in zip(self.genes, other.genes):
            chosen = g1 if random.random() < 0.5 else g2
            child_genes.append(
                ScheduledEvent(chosen.event, chosen.day, chosen.room_index, chosen.start)
            )
        return Individual(self.data, child_genes)

    def mutate(self, rate):
        for g in self.genes:
            if random.random() < rate:
                op = random.randint(0, 2)
                if op == 0:
                    g.day = random.randint(0, 4)
                elif op == 1:
                    g.room_index = random.randint(0, len(self.data.rooms) - 1)
                else:
                    ev = g.event
                    latest = END_MINUTES - ev.duration
                    slots = (latest - START_MINUTES) // TIME_STEP + 1
                    slot = random.randint(0, slots - 1)
                    g.start = START_MINUTES + slot * TIME_STEP

        self.fitness = None