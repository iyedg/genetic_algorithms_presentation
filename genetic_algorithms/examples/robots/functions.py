import numpy as np
import random
from .chromosomes import Robot, PowerSource, Motor


def fitness(individual):
    return (
        individual.specific_power * 10 ** 3
        - individual.weight
        - (individual.motor.power - individual.power_source.power) ** 2
    )


def random_robot():
    # Choose two integers between 0 and 7 then generate a power source
    # and a motor from them
    motor = Motor.from_binary(np.binary_repr(np.random.randint(0, 8)))
    power_source = PowerSource.from_binary(np.binary_repr(np.random.randint(0, 8)))
    return Robot(power_source=power_source, motor=motor)


def pick_random_parents(pop):
    """
    This is how we are going to select parents from the population
    """
    mom = random.choice(pop)
    dad = random.choice(pop)
    return mom, dad


def make_child(mom, dad):
    """
    This function describes how two candidates combine into a
    new candidate. Note that the output is a tuple, just like
    the output of `random_start`. We leave it to the developer
    to ensure that chromosomes are of the same type.
    """
    # TODO: add breed method
    mom_binary = mom.as_binary()
    dad_binary = dad.as_binary()
    index = np.random.randint(0, 7)
    child_binary = f"{mom_binary[:index]}{dad_binary[index:]}"
    return Robot.from_binary(child_binary)


def mutate(chromosome, sigma):
    """
    Toggle one bit at random
    """
    cutoff = abs(np.random.normal())
    # cutoff = 2
    if cutoff > 1:
        binary_as_list = list(chromosome.as_binary())
        bit_1 = np.random.randint(0, 6)
        # bit_2 = np.random.randint(0, 6)
        binary_as_list[bit_1] = str(1 - int(binary_as_list[bit_1]))
        # binary_as_list[bit_2] = str(1 - int(binary_as_list[bit_2]))
        return Robot.from_binary("".join(binary_as_list))
    else:
        return chromosome
