from roguelife.game.game import Game
from roguelife.evo.evo import EvoAlg
from roguelife.agents.rulebased import RuleBasedAgent0, RuleBasedAgent1, RuleBasedAgent2, RuleBasedAgent3, RandomAgent
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
    },
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

ea = EvoAlg(gen_param_specs)
env = Game(evo_system=ea)
state = env.reset()

agent_classes = {
    'R01' : RuleBasedAgent0,
    'R02' : RuleBasedAgent1,
    'R03' : RuleBasedAgent2,
    'R04' : RuleBasedAgent3,
    'RR' : RandomAgent
}


generations = 30

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
            