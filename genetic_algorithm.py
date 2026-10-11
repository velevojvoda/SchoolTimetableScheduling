import random

from individual import Individual
from data_loader import TimetableData


class GeneticAlgorithm:
    def __init__(
        self,
        data: TimetableData,
        population_size=80,
        generations=200,
        crossover_rate=0.9,
        mutation_rate=0.1,
        elitism_size=2,
        tournament_size=3,
        random_seed=None
    ):
        self.data = data
        self.population_size = population_size
        self.generations = generations
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.elitism_size = elitism_size
        self.tournament_size = tournament_size

        if random_seed is not None:
            random.seed(random_seed)

        self.population = []

    def _init_population(self):
        self.population = [Individual(self.data) for _ in range(self.population_size)]

    def _tournament(self):
        comp = random.sample(self.population, self.tournament_size)
        return max(comp, key=lambda ind: ind.evaluate_fitness())

    def run(self):
        self._init_population()
        best = max(self.population, key=lambda ind: ind.evaluate_fitness())

        for _ in range(self.generations):
            new_pop = sorted(
                self.population, key=lambda ind: ind.evaluate_fitness(), reverse=True
            )[: self.elitism_size]

            while len(new_pop) < self.population_size:
                p1 = self._tournament()
                p2 = self._tournament()
                child = p1.crossover(p2) if random.random() < self.crossover_rate else p1.clone()
                child.mutate(self.mutation_rate)
                new_pop.append(child)

            self.population = new_pop
            best_now = max(self.population, key=lambda ind: ind.evaluate_fitness())
            if best_now.evaluate_fitness() > best.evaluate_fitness():
                best = best_now

        return best