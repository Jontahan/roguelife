from evo.evo import EvoAlg
from game.game import Game
import random
import time
from run_full import gen_param_specs

dummyEvoSystem = EvoAlg(spec=gen_param_specs)
env = Game(evo_system=dummyEvoSystem)

while True:
    pil_image, reward, done, thing = env.step(env.action_space.sample())
    if done:
        env.reset()
