import json
import matplotlib.pyplot as plt
import sys

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
			phistories[key].append(((sum(arr) / len(arr)) - data['spec'][key]['min']) / (vrange if vrange != 0 else data['spec'][key]['min']))

fig = plt.figure(1)
for key in phistories:
	if key != "base_clear_depth" and key != "random_seed":
		print(key)
		plt.plot(phistories[key], label=key)
plt.legend(loc='center left', bbox_to_anchor=(1, .5))
plt.title('{} evolution'.format(data_id))
fig.savefig('{}_plot'.format(data_id), bbox_inches='tight')