
from game.game import Game
from evo.evo import EvoAlg
from agents.rulebased import RuleBasedAgent0, RuleBasedAgent1, RuleBasedAgent2, RuleBasedAgent3
import random 
import random 
import time

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

random.seed(47)

ea = EvoAlg(gen_param_specs)
env = Game(evo_system=ea)
state = env.reset()
agent = RuleBasedAgent3(env)

while True:
    state, _, done, _ = env.step(agent.act(state))
    time.sleep(0.1)
    
    if done:
        env.reset()
        agent = RuleBasedAgent3(env)