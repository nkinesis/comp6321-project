import numpy as np
import pandas as pd

alg_values = ["ppo", "a2c", "dqn"]
step_values = ["10000", "50000", "100000", "500000", "1000000"]
rew_values = ["break-and-follow", "break", "follow"]

base_path = "testing/rounds/round1/scores/"
ds_b = pd.read_csv(base_path + "b20.csv", sep=",")
ds_f = pd.read_csv(base_path + "f20.csv", sep=",")
ds_bf = pd.read_csv(base_path + "bf20.csv", sep=",")

def get_dataset(reward):
    if reward == "break-and-follow":
        return ds_bf
    elif reward == "break":
        return ds_b
    return ds_f
    
def get_max_min(score_avgs, lives_avgs, combination):
    max_score = max(score_avgs)
    max_lives = max(lives_avgs)
    min_score = min(score_avgs)
    min_lives = min(lives_avgs)

    top = 5
    row = {}
    row['max_score'] = max_score
    row['max_lives'] = max_lives
    row['min_score'] = min_score
    row['min_lives'] = min_lives
    row['max_score_from'] = combination[score_avgs.index(max_score)]
    row['max_lives_from'] = combination[lives_avgs.index(max_lives)]
    row['min_score_from'] = combination[score_avgs.index(min_score)]
    row['min_lives_from'] = combination[lives_avgs.index(min_lives)]
    row['top_scores'] = get_top_x(np.array(score_avgs), top)
    row['top_lives'] = get_top_x(np.array(lives_avgs), top)
    return row
    
def get_top_x(arr, x):
    return arr[np.argpartition(arr, -x)[-x:]]

def get_avg_by_algorithm():
    score_avgs = []
    lives_avgs = []
    combination = []
    results = []
    for a in alg_values:
        row = {}
        for r in rew_values:
            ds = get_dataset(r)
            combination.append(a + " | " + r)
            filtered = ds[(ds.algorithm.str.contains(a))] 
            s = filtered["score"].mean()
            l = filtered["lives"].mean()
            score_avgs.append(s)
            lives_avgs.append(l)        
            row['combination'] = a + " | " + r
            row['avg_score'] = s
            row['avg_lives'] = l
            results.append(row)
        
    results.append(get_max_min(score_avgs, lives_avgs, combination))
    return results

def get_avg_by_steps():
    score_avgs = []
    lives_avgs = []
    combination = []
    results = []
    for step in step_values:
        row = {}
        for r in rew_values:
            ds = get_dataset(r)
            combination.append(str(step) + " | " + r)
            filtered = ds[(ds.algorithm.str.contains("_" + str(step)))]
            s = filtered["score"].mean()
            l = filtered["lives"].mean()
            score_avgs.append(s)
            lives_avgs.append(l)
            row['combination'] = str(step) + " | " + r
            row['avg_score'] = s
            row['avg_lives'] = l
            results.append(row)
            
    results.append(get_max_min(score_avgs, lives_avgs, combination))
    return results

def get_avg_by_alg_steps():
    score_avgs = []
    lives_avgs = []
    combination = []
    results = []
    for a in alg_values:
        row = {}
        for step in step_values:
            for r in rew_values:
                ds = get_dataset(r)
                combination.append(str(step) + " | " + a + " | " + r)
                filtered = ds[(ds.algorithm.str.contains("_" + str(step)) & ds.algorithm.str.contains(a))]
                s = filtered["score"].mean()
                l = filtered["lives"].mean()
                score_avgs.append(s)
                lives_avgs.append(l)
                row['combination'] = str(step) + " | " + a + " | " + r
                row['avg_score'] = s
                row['avg_lives'] = l
                results.append(row)
        
    results.append(get_max_min(score_avgs, lives_avgs, combination))
    return results

if __name__ == "__main__":
    print(get_avg_by_alg_steps())