import glob
import json
import matplotlib.pyplot as plt
import sys
from game.game import Game
from evo.evo import EvoAlg
from agents.rulebased import RuleBasedAgent0, RuleBasedAgent1, RuleBasedAgent2, RuleBasedAgent3, RandomAgent


agent_types = ["R01", "R02", "R03", "R04"]


agent_classes = {
	'R01' : RuleBasedAgent0,
	'R02' : RuleBasedAgent1,
	'R03' : RuleBasedAgent2,
	'R04' : RuleBasedAgent3,
	'RR' : RandomAgent
}


agent_plot_files = []

for agent in agent_types:
	agent_plot_files.append(glob.glob("./Plots/" + agent + "*log.txt"))


print(agent_plot_files)


for i in range(len(agent_types)):
	print("\n\nLevels Generated for " + agent_types[i] + ": \n\n\n")

	for j in range(len(agent_types)):

		print("Fitness of " + agent_types[j] + ": \n")
		total_reward = 0
		for plot_file_num in range(len(agent_plot_files[i])):

			with open(agent_plot_files[i][plot_file_num]) as f:
				data = json.load(f)
			sum_reward = 0
			for level in data['population_history'][-1]['population']:
				gen_param_specs = {
					'initial_rock_density' : {
						'dtype' : float,
						'min' : level['initial_rock_density'],
						'max' : level['initial_rock_density']
					},
					'initial_tree_density' : {
						'dtype' : float,
						'min' : level['initial_tree_density'],
						'max' : level['initial_tree_density']
					},
					'rock_refinement_runs' : {
						'dtype' : int,
						'min' : level['rock_refinement_runs'],
						'max' : level['rock_refinement_runs']
					},
					'tree_refinement_runs' : {
						'dtype' : int,
						'min' : level['tree_refinement_runs'],
						'max' : level['tree_refinement_runs']
					},
					'rock_neighbour_depth' : {
						'dtype' : int,
						'min' : level['rock_neighbour_depth'],
						'max' : level['rock_neighbour_depth']
					},
					'tree_neighbour_depth' : {
						'dtype' : int,
						'min' : level['tree_neighbour_depth'],
						'max' : level['tree_neighbour_depth']
					},
					'rock_neighbour_number' : {
						'dtype' : int,
						'min' : level['rock_neighbour_number'],
						'max' : level['rock_neighbour_number']
					},
					'tree_neighbour_number' : {
						'dtype' : int,
						'min' : level['tree_neighbour_number'],
						'max' : level['tree_neighbour_number']
					},
					'base_clear_depth' : {
						'dtype' : int,
						'min' : level['base_clear_depth'],
						'max' : level['base_clear_depth']
					},
					'enemies_crush_trees' : {
						'dtype' : bool
					},
					'random_seed' : {
						'dtype' : int,
						'min' : level['random_seed'],
						'max' : level['random_seed']
					},
					'flee_distance' : {
						'dtype' : int,
						'min' : level['flee_distance'],
						'max' : level['flee_distance']
					}
				}


				ea = EvoAlg(gen_param_specs)
				env = Game(evo_system=ea)
				state = env.reset()

				run_limit = 1

				
				agent_class = agent_classes[agent_types[j]]
				agent = agent_class(env)
				reward_count = 0
				while True:
					state, reward, done, _ = env.step(agent.act(state))
					reward_count += reward

					if done:
						#print(reward_count)
						break
				sum_reward += reward_count


			print("Average reward for run ", plot_file_num, " : ", sum_reward/100)
			total_reward += sum_reward/100

		print("Total average reward over the ", len(agent_plot_files[i]) ," runs: ", total_reward/len(agent_plot_files[i]))

					#We need to average this so we have the average for each agent type 
							


