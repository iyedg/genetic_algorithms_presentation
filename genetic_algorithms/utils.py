from tqdm import tqdm_notebook

class MyLogger:
    def __init__(self, generations=200):
        self.iteration = 0
        self.generations = generations
        self.individuals_by_generation = []
        self.t = tqdm_notebook(total=generations, unit="generation", disable=False)

    def log(self, pop):
        self.iteration += 1
        self.t.update()
        for i in pop.evaluate():
            choices = i.chromosome
            individual_fitness = i.fitness
            self.individuals_by_generation.append(
                {
                    "generation": self.iteration,
                    "choices": choices,
                    "individual_fitness": individual_fitness
                }
            )
        if self.iteration == self.generations:
            self.t.close()