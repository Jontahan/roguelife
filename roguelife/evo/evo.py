import random
import numpy as np

class EvoAlg:
    def __init__(self, spec):
        # Tuning parameters
        self.spec = spec
        self.population_size = 100
        self.truncation_selection = int(self.population_size * .3)
        self.mutation_rate = .05
        self.generation = 0

    # For the first batch
    def get_initial_population(self):
        pop = []
        for _ in range(self.population_size):
            individual = {}
            for key in self.spec:
                if self.spec[key]['dtype'] == float:
                    individual[key] = random.uniform(self.spec[key]['min'], self.spec[key]['max'])
                if self.spec[key]['dtype'] == int:
                    individual[key] = random.randint(self.spec[key]['min'], self.spec[key]['max'])
                if self.spec[key]['dtype'] == bool:
                    individual[key] = True
            pop.append(individual)
        return pop

    def get_new_generation(self, population):
        population.sort(reverse=True, key=lambda x: x[1])
        # print("Population: ", population)
        # print("POP1: ", population[0])
        
        # Select best and strip off fitness
        parents = [x[0] for x in population[:self.truncation_selection]]
        new_pop = []
        
        for _ in range(self.population_size):
            temp = parents[random.randint(0, len(parents) - 1)].copy()
            # Mutation
            for key in temp:
                if random.uniform(0, 1) < self.mutation_rate:
                    if self.spec[key]['dtype'] == float:
                        temp[key] = random.uniform(self.spec[key]['min'], self.spec[key]['max'])
                    if self.spec[key]['dtype'] == int:
                        temp[key] = random.randint(self.spec[key]['min'], self.spec[key]['max'])
                    if self.spec[key]['dtype'] == bool:
                        temp[key] = True
            new_pop.append(temp)
        
        return new_pop

# Placeholder, fitness should come from game
def fitness_function(population):
    out = []
    for individual in population:
        fitness = sum([individual[key] for key in individual]) / len(individual.keys())
        out.append((individual, fitness))
    return out

if __name__ == '__main__':
    # Simple numerical optimization to see if the system converges in a trivial context
    ea = EvoAlg({
        'a' : {'dtype' : float, 'min' : 0.0, 'max' : 1.0},
        'b' : {'dtype' : float, 'min' : 0.0, 'max' : 1.0}
    })
    pop = ea.get_initial_population()

    for geni in range(100):
        print("Generation: ", geni)
        pop_fit = fitness_function(pop)
        avg_fit = sum([i[1] for i in pop_fit])/len(pop_fit)
        print("Average Fitness: ", avg_fit)
        pop = ea.get_new_generation(pop_fit)
