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
            individual_motor = i.chromosome.motor
            individual_power_source = i.chromosome.power_source
            individual_fitness = i.fitness
            self.individuals_by_generation.append(
                {
                    "generation": self.iteration,
                    "individual_motor": individual_motor,
                    "individual_power_source": individual_power_source,
                    "individual_fitness": individual_fitness,
                }
            )
        if self.iteration == self.generations:
            self.t.close()