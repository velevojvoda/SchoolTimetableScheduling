from data_loader import TimetableData
from genetic_algorithm import GeneticAlgorithm
from utils import print_timetable


def main():
    DATA_FILE = "data_timetable.txt"

    data = TimetableData.from_file(DATA_FILE)
    print(f"Učitano {len(data.rooms)} učionica i {len(data.events)} događaja.")

    ga = GeneticAlgorithm(
        data=data,
        population_size=80,
        generations=200,
        crossover_rate=0.9,
        mutation_rate=0.1,
        elitism_size=2,
        tournament_size=3,
        random_seed=42,
    )

    best = ga.run()
    print(f"\nNajbolji fitnes: {best.evaluate_fitness():.2f}\n")

    print_timetable(best, data)


if __name__ == "__main__":
    main()