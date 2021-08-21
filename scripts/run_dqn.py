from game.game import Game
from evo.evo import EvoAlg
from os import path
import random 
import time
import sys

from stable_baselines3 import DQN
from stable_baselines3.common.vec_env import DummyVecEnv

gen_param_specs = {
    'initial_rock_density' : {
        'dtype' : float,
        'min' : 0.2,
        'max' : 0.4
    },
    'initial_tree_density' : {
        'dtype' : float,
        'min' : 0.2,
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

random.seed(42)

ea = EvoAlg(gen_param_specs)
env_raw = Game(evo_system=ea)
env = DummyVecEnv([lambda : env_raw])

if len(sys.argv) == 3 and sys.argv[1] == '--train':
    if path.exists('saved_models/{}.zip'.format(sys.argv[2])):
        model = DQN.load('saved_models/{}'.format(sys.argv[2]), env=env)
        print('Loading existing model')
    else:
        print('Creating new model')
        model = DQN('CnnPolicy', env, verbose=1, buffer_size=1000, learning_starts=1000, exploration_fraction=0.3)
    try:
        model.learn(total_timesteps=100000, log_interval=4)
        model.save('saved_models/{}'.format(sys.argv[2]))
        env_raw.worldgen.save_log(sys.argv[2])
    except:
        model.save('saved_models/{}'.format(sys.argv[2]))
        env_raw.worldgen.save_log(sys.argv[2])

if len(sys.argv) == 3 and sys.argv[1] == '--run':
    model = DQN.load('saved_models/{}'.format(sys.argv[2]), env=env)
    obs = env.reset()

    while True:
        action, _ = model.predict(obs, deterministic=False)
        obs, reward, done, info = env.step(action)

        if done:
            obs = env.reset()
