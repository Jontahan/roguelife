import json
import matplotlib.pyplot as plt
import sys

data_id = sys.argv[1]
frame_size = 1000
with open('{}_reward.txt'.format(data_id)) as f:
    rewards = [float(line)for line in f.readlines()]
    avg_rewards = []
    tmp = 0
    for i, val in enumerate(rewards):
        tmp += val
        if i > 0 and i % frame_size == 0:
            avg_rewards.append(tmp / frame_size)
            print("Average Reward: ", tmp / frame_size)
            tmp = 0
        
    plt.plot(avg_rewards)
    plt.title('{} reward'.format(data_id))
    plt.savefig('{}_reward_plot'.format(data_id))
