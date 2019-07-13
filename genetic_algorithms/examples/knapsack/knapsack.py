import attr
import numpy as np
from .test_instance import test_instance
from loguru import logger


@attr.s
class Knapsack:
    capacity: int = attr.ib()
    n_items: int = attr.ib()

    @classmethod
    def from_literature(cls):
        # z = 1428
        knapsack = cls(capacity=970, n_items=20)
        knapsack.items = np.array(test_instance)
        return knapsack

    @classmethod
    def from_params(cls):
        pass

    def get_solutions(self, size):
        """Randomly generate a solution to the current Knapsack problem.
        The solution(s) generated may not be feasible and are not necessarily unique.

        Arguments:
            size {int} -- The number of solutions to be generated

        Returns:
            np.ndarray -- A list containing randomly generated solutions
        """
        return np.array(
            [np.random.randint(low=0, high=2, size=self.n_items) for _ in range(size)]
        )

    @property
    def items(self):
        return self.__items

    @items.setter
    def items(self, value):
        # perhaps some validation here
        self.__items = value

    def fitness(self, chromosome):
        chosen_items = self.items[[bool(i) for i in chromosome]]
        sum_weights = sum([i["weight"] for i in chosen_items])
        sum_values = sum([i["value"] for i in chosen_items])

        rho = max([i["value"] / i["weight"] for i in self.items])

        penalty = rho * sum_weights - self.capacity
        penalize = int(sum_weights > self.capacity)

        return sum_values - penalize * penalty

    def select(self, population):
        # elitist selector
        sorted_by_fitness = sorted(population, key=lambda x: x.fitness, reverse=True)
        return np.random.choice(sorted_by_fitness[:10], 2)

    def crossover(self, father, mother):
        m = np.random.randint(0, self.n_items, size=2)
        child = np.concatenate(
            [father[: min(m)], mother[min(m) : max(m)], father[max(m) :]]
        )
        return child
