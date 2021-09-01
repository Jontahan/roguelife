
from game.game import Game
from evo.evo import EvoAlg
from agents.rulebased import RuleBasedAgent0, RuleBasedAgent1, RuleBasedAgent2, RuleBasedAgent3, RandomAgent
import random 
import time
import sys

gen_param_specs = {
    'initial_rock_density' : {
        'dtype' : float,
        'min' : 0.1,
        'max' : 0.4
    },
    'initial_tree_density' : {
        'dtype' : float,
        'min' : 0.1,
        'max' : 0.4
    },
    'rock_refinement_runs' : {
        'dtype' : int,
        'min' : 1,
        'max' : 3
    },
    'tree_refinement_runs' : {
        'dtype' : int,
        'min' : 1,
        'max' : 3
    },
    'rock_neighbour_depth' : {
        'dtype' : int,
        'min' : 1,
        'max' : 2
    },
    'tree_neighbour_depth' : {
        'dtype' : int,
        'min' : 1,
        'max' : 2
    },
    'rock_neighbour_number' : {
        'dtype' : int,
        'min' : 4,
        'max' : 8
    },
    'tree_neighbour_number' : {
        'dtype' : int,
        'min' : 4,
        'max' : 8
    },
    'base_clear_depth' : {
        'dtype' : int,
        'min' : 1,
        'max' : 1
    },
    'enemies_crush_trees' : {
        'dtype' : bool
    }
    ,
    'random_seed' : {
        'dtype' : int,
        'min' : 1,
        'max' : 9999
    },
    'flee_distance' : {
        'dtype' : int,
        'min' : 0,
        'max' : 10
    }
}



class RandomEvo:
    def __init__(self, spec):
        # Tuning parameters
        self.spec = spec
        self.population_size = 1000


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

        return self.get_initial_population()










ea = RandomEvo(gen_param_specs)
env = Game(evo_system=ea)
state = env.reset()

agent_classes = {
    'R01' : RuleBasedAgent0,
    'R02' : RuleBasedAgent1,
    'R03' : RuleBasedAgent2,
    'R04' : RuleBasedAgent3,
    'RR' : RandomAgent
}


generations = 1

run_limit = generations * ea.population_size

if len(sys.argv) == 4 and sys.argv[1] == '--run':
    agent_class = agent_classes[sys.argv[2]]
    agent = agent_class(env)
    i = 0
    reward_count = 0
    reward_history = []
    while True:
        state, reward, done, _ = env.step(agent.act(state))
        reward_count += reward

        if done:
            reward_history.append(reward_count)
            reward_count = 0
            env.reset()
            i += 1
            agent = agent_class(env)
            if i > run_limit:
                f = open('{}_reward.txt'.format(sys.argv[3]), 'a')
                for value in reward_history:
                    f.write('{}\n'.format(value))
                f.close()

                env.worldgen.save_log(sys.argv[3])
                quit()
            