import json
import matplotlib.pyplot as plt
import sys
import glob
import numpy as np

frame_size = 100

agent_types = ["R01", "R02", "R03", "R04"]

agent_reward_files = []



for agent in agent_types:
    agent_reward_files.append(glob.glob("./Plots_S/S" + agent + "*reward.txt"))

all_agents_rewards_list = []

for agent_num in range(len(agent_types)):

    reward_files = agent_reward_files[agent_num]

    rewards_list = []

    for file in reward_files:

        with open(file) as f:
            counter = 0
            rewards = [float(line)for line in f.readlines()]
            avg_rewards = []
            tmp = 0
            for i, val in enumerate(rewards):
                tmp += val
                if i > 0 and i % frame_size == 0:
                    avg_rewards.append(tmp / frame_size)
                    tmp = 0
                    counter+=1
            rewards_list.append(avg_rewards)

    all_agents_rewards_list.append(rewards_list)

print(all_agents_rewards_list)


agents_deviation_list = []
agents_avg_reward_list = []

for agent_num in range(len(agent_types)):

    agent_reward_list = all_agents_rewards_list[agent_num]

    avg_reward_list = []

    deviation_list = []

    for i in range(len(agent_reward_list[0])):
        total_reward = 0
        data_list = []
        for j in range(len(agent_reward_list)):
            total_reward += agent_reward_list[j][i]
            data_list.append(agent_reward_list[j][i])

        deviation_list.append(np.std(data_list))
        avg_reward_list.append(total_reward/len(agent_reward_list))

    agents_deviation_list.append(deviation_list)
    agents_avg_reward_list.append(avg_reward_list)

colours = ['#377eb8', '#ff7f00', '#4daf4a', '#f781bf']

agents_top_list = []
agents_bot_list = []

for agent_num in range(len(agent_types)):

    top_list = []

    bot_list = []

    for i in range(len(agent_reward_list[0])):

        top_list.append(agents_avg_reward_list[agent_num][i] + agents_deviation_list[agent_num][i])
        bot_list.append(agents_avg_reward_list[agent_num][i] - agents_deviation_list[agent_num][i])
    agents_top_list.append(top_list)
    agents_bot_list.append(bot_list)

for agent_num in range(len(agent_types)):

    plt.plot(range(1,31), agents_avg_reward_list[agent_num], color = colours[agent_num], label=agent_types[agent_num])
    plt.fill_between(x=range(1,31), y1=agents_bot_list[agent_num], y2=agents_top_list[agent_num], color = colours[agent_num], alpha=0.15)
    plt.legend()
axes = plt.gca()
axes.set_ylim([-10,2])
plt.title("Average Reward for all Agents (\"Hardcore\" Scenario) Evolving Only Seed")
plt.savefig("average_reward_all_seed_only")
    #plt.clf()
































