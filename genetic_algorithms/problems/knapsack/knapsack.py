import attr
import numpy as np
from loguru import logger
import pulp
import pandas as pd


@attr.s
class Knapsack:
    n_items: int = attr.ib()
    capacity: int = attr.ib(default=None)
    __items = None
    __weights = None
    __values = None

    @property
    def items(self):
        if self.__items is None:
            self.__items = []
            for value, weight in zip(self.values, self.weights):
                self.__items.append({"value": value, "weight": weight})
        # Not the most efficient to convert it on each call
        return np.array(self.__items)

    @property
    def weights(self):
        if self.__weights is None:
            # TODO: magic value
            self.__weights = np.random.randint(1, 100, size=self.n_items)
        return self.__weights

    @property
    def values(self):
        if self.__values is None:
            # TODO: magic value
            self.__values = [
                weight + np.random.randint(0, 100, size=self.n_items)
                for weight in self.weights
            ]
        return self.__values

    def solution_candidate(self):
        return np.random.randint(0, 2, size=self.n_items)

    def solution_value(self, solution):
        try:
            return np.sum(np.array(solution) * self.values)
        except:
            import ipdb

            ipdb.set_trace()

    def solution_weight(self, solution):
        return np.sum(np.array(solution) * self.weights)

    def is_feasible(self, solution):
        return self.solution_weight(solution) < self.capacity

    def solution_penalty(self, solution):
        rho = np.max(self.values / self.weights)
        return (1 - self.is_feasible(solution)) * (
            rho * self.solution_weight(solution) - self.capacity
        )

    def solution_fitness(self, solution):
        return self.solution_value(solution) - self.solution_penalty(solution)

    def crossover(self, *parents, **kwargs):
        # TODO: implicitly assuming two parents, improve
        mother, father = parents
        if not kwargs.get("crossover_rate"):
            crossover_rate = 1
        else:
            crossover_rate = kwargs.get("crossover_rate")
        if np.random.random() < crossover_rate:
            m = np.random.randint(0, self.n_items)
            return np.concatenate((mother[:m], father[m:]))
        else:
            return np.random.choice(parents)

    def select(self, population):
        return np.random.choice(population, 2, replace=False)

    def lp_solve(self):
        data = pd.DataFrame.from_records(self.items)
        items = data.index
        self.lp = pulp.LpProblem("Knapsack problem", pulp.LpMaximize)
        # Decision variable: binary denoting wether to include an item or not
        x = pulp.LpVariable.dicts(
            "include_item", range(self.n_items), cat=pulp.LpBinary
        )
        # Objective function
        self.lp += pulp.lpSum([data.iloc[i, 0] * x[i] for i in items])
        # Capacity constraint
        self.lp += pulp.lpSum([data.iloc[i, 1] * x[i] for i in items]) <= self.capacity
        self.lp.solve()
        logger.debug(pulp.LpStatus[self.lp.status])
        return self.lp, x
