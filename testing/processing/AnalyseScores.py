import sys
import numpy as np
import pandas as pd

ds = pd.read_csv(sys.argv[1], sep=',')
list_algs_names = ["ppo", "a2c", "dqn"]
list_steps = [10000, 50000, 100000, 500000, 1000000]
line_score = []
line_lives = []

for i in range(0, len(list_algs_names)):
    for j in range(0, len(list_steps)):
        ds_filtered = ds[(ds['algorithm'].str.contains(list_algs_names[i] + "_" + str(list_steps[j])))]
        avg_score = np.round(np.average(ds_filtered['score'].values), 2)
        avg_lives = np.round(np.average(ds_filtered['lives'].values), 2)

        #print(list_algs_names[i], list_steps[j], "score:", avg_score, "| lives:", avg_lives)
        line_score.append(avg_score)
        line_lives.append(avg_lives)
    print(list_algs_names[i])
    print(line_score)
    print(line_lives)
    line_score = []
    line_lives = []