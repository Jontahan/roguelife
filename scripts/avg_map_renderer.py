from game.game import Game
from evo.evo import EvoAlg
from run_log import gen_param_specs 
import sys
import json

data_id = sys.argv[1]

with open('{}_log.txt'.format(data_id)) as f:
    data = json.load(f)

phistories = {}
for key in data['spec']:
    if 'min' in data['spec'][key]:
        phistories[key] = []

for pop in data['population_history']:
    for key in data['spec']:
        arr = [param[key] for param in pop['population']]

        if 'min' in data['spec'][key]:
            vrange = data['spec'][key]['max'] - data['spec'][key]['min']
            value = sum(arr) / len(arr)
            if gen_param_specs[key]['dtype'] == int:
                value = round(value)
            phistories[key].append(value)

last_avg_param = {}
for key in phistories:
    last_avg_param[key] = phistories[key][-1]
last_avg_param['enemies_crush_trees'] = True

ea = EvoAlg(gen_param_specs)
env = Game(evo_system=ea)
env.worldgen.level_params = [last_avg_param]
state = env.reset()
env.screenshot('{}_render'.format(data_id))
