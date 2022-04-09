import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

""" All functions were written by Gabriel C. Ullmann, unless otherwise noted.
Algorithms, steps and rewards used in the tests"""
alg_values = ["ppo", "a2c", "dqn"]
rew_values = ["break-and-follow", "break", "follow"]

""" Colors used in the plots"""
c1 = "#ee442f"
c2 = "#601a4a"
c3 = "#63acbe"
c4 = "#000000"

""" Path to file with aggregated results across all rounds """
base_path = "testing/rounds/"
ds_all = pd.read_csv(base_path + "all.csv", sep=",")

""" Averages for all combination of reward, algorithm, steps
Generated using script 4_compute_avg_scores.py """
ds_bf = {
    'ppo': {
        'scores': [108.72, 99.92, 120.25, 104.17, 134.33],
        'lives': [4.58, 5.0, 4.38, 5.0, 4.12]
    },
    'a2c': {
        'scores': [91.0, 94.17, 81.75, 87.67, 68.67],
        'lives': [4.2, 3.5, 3.82, 3.23, 2.63]
    },
    'dqn': {
        'scores': [51.78, 62.92, 77.67, 93.17, 126.5],
        'lives': [1.71, 2.07, 2.57, 3.85, 3.83]
    }
}
ds_b = {
    'ppo': {
        'scores': [28.5, 23.17, 26.5, 20.5, 43.67],
        'lives': [0.57, 0.13, 0.58, 0.15, 1.12]
    },
    'a2c': {
        'scores': [10.67, 12.42, 9.25, 12.5, 11.33],
        'lives': [0.08, 0.08, 0.08, 0.07, 0.12]
    },
    'dqn': {
        'scores': [13.28, 23.83, 14.0, 35.17, 9.0],
        'lives': [0.08, 0.17, 0.08, 0.25, 0.03]
    }
}
ds_f = {
    'ppo': {
        'scores': [98.11, 112.58, 99.17, 104.83, 106.0],
        'lives': [4.83, 4.53, 4.75, 4.4, 4.58]
    },
    'a2c': {
        'scores': [74.5, 53.42, 56.08, 41.67, 10.33],
        'lives': [3.09, 1.64, 2.16, 0.87, 0.1]
    },
    'dqn': {
        'scores': [46.22, 60.83, 52.42, 109.33, 52.0],
        'lives': [1.86, 2.51, 2.25, 4.95, 2.87]
    }
}

""" Convert string array to uppercase.

Arguments
---------
arr : array
    Array of strings.

Returns
---------
    Array of uppercase strings.
"""


def to_uppercase(arr):
    arr_upper = []
    for item in arr:
        arr_upper.append(item.upper())
    return arr_upper


""" Filter 'all rounds' dataset by reward scenario.
If no reward informed, return full dataset.

Arguments
---------
reward : string
    Name of the reward scenario (e.g. break-and-follow).

Returns
---------
    A pandas.DataFrame object, filtered by reward or not.
"""


def get_ds_all_rounds(reward=None):
    if reward is None:
        return ds_all
    else:
        return ds_all[(ds_all.reward == reward)]


"""  Get dataset of averages related to a reward scenario.

Arguments
---------
reward : string
    Name of the reward scenario (e.g. break-and-follow).

Returns
---------
    A pandas.DataFrame object, filtered by reward or not.
"""


def get_ds_by_reward(reward):
    if reward == "break-and-follow":
        return ds_bf
    elif reward == "break":
        return ds_b
    return ds_f


""" Get color related to a given algorithm in the plots.

Arguments
---------
alg : string
    Name of the algorithm (e.g. ppo).

Returns
---------
    A HEX color code in string form.
"""


def get_color(alg):
    if alg == "ppo" or alg == "PPO":
        return c1
    elif alg == "a2c" or alg == "A2C":
        return c2
    elif alg == "dqn" or alg == "DQN":
        return c3
    return c4


""" Draw matplotlib bar plot

Arguments
---------
order : int
    Order of appearance of the subplot inside the bigger plot. Ranges from 1 to 6.
arr_params : array
    List of parameters, X-axis of the plot.
arr_avgs : array
    List of score/live averages, Y-axis of the plot.
title : string
    Plot title.
y_label : string
    Label of the Y-axis (score/lives).
y_max : float
    Maximum value to be displayed in the Y-axis. Used to adjust the height of the plot.
"""


def draw_bar_plot(order, arr_params, arr_avgs, title, y_label, y_max):
    plt.subplot(2, 3, order)
    if "ppo" in arr_params:
        plot = plt.bar(to_uppercase(arr_params), arr_avgs, color=[c1, c2, c3])
    else:
        plot = plt.bar(arr_params, arr_avgs, color=[c3])
    plt.bar_label(plot, np.around(arr_avgs, 2))
    plt.ylabel(y_label)
    plt.title("(%s) %s, %s" % (chr(order + 96), title, y_label))
    plt.ylim(0, y_max)
    plt.tight_layout()


""" Generate line plot comparing score/live average by reward vs. algorithms vs. steps """


def generate_comparison_line():
    count = 1
    var_values = ["scores", "lives"]
    step_values = ["10K", "50K", "100K", "500K", "1M"]
    plt.figure(figsize=(12, 6))
    for v in var_values:
        for r in rew_values:
            for a in alg_values:
                d = get_ds_by_reward(r)
                plt.subplot(2, 3, count)
                plt.plot(step_values, d[a][v],
                         color=get_color(a), label=a.upper())
                plt.title("(" + chr(count + 96) + ") " + r + ", " + v)
                plt.xlabel("steps")
                plt.ylabel("score" if v == "scores" else v)
                plt.legend(loc="right")
                plt.ylim(0, 140) if v == "scores" else plt.ylim(0, 5.2)
                plt.tight_layout()
            count += 1

    plt.savefig("docs/img/all_combinations.pdf")


""" Generate bar plot comparing score/live average by reward vs. algorithms vs. steps """


def generate_comparison_bars():
    step_values = ["10000", "50000", "100000", "500000", "1000000"]
    list_params = [rew_values, alg_values, step_values]
    list_params_names = ["rewards", "algorithm", "steps"]
    plt.figure(figsize=(12, 6))
    index = 0
    for param in list_params:
        avgs_score = []
        avgs_lives = []
        for p in param:
            if list_params_names[index] == "rewards":
                ds = get_ds_all_rounds(p)
            elif list_params_names[index] == "algorithm":
                ds = get_ds_all_rounds()
                ds = ds[(ds.algorithm.str.contains(p))]
            else:
                ds = get_ds_all_rounds()
                ds = ds[(ds.algorithm.str.contains("_" + str(p)))]
            avgs_score.append(ds["score"].mean())
            avgs_lives.append(ds["lives"].mean())
        draw_bar_plot(
            index + 1,
            param,
            avgs_score,
            list_params_names[index],
            "score",
            100)
        draw_bar_plot(
            index + 4,
            param,
            avgs_lives,
            list_params_names[index],
            "lives",
            4)
        index += 1

    plt.savefig("docs/img/all_avgs.pdf")


""" Generate table with combination of top scores/lives

Arguments
---------
min_score : int
    Filter by scores greater than this

min_lives : int
    Filter by number of lives greater than this
"""


def generate_top_scores_table(min_score=250, min_lives=3):
    ds = get_ds_all_rounds()
    tops = ds[(ds.score > min_score) & (ds.lives >= min_lives)]
    tops = tops.sort_values('score', ascending=False)
    tops.to_csv('docs/top_scores_table.csv', index=False)


if __name__ == "__main__":
    generate_comparison_line()
    generate_comparison_bars()
    generate_top_scores_table()
