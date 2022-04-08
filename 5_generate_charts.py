import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

c1 = "#ee442f"
c2 = "#601a4a"
c3 = "#63acbe"
alg_values = ["ppo", "a2c", "dqn"]
step_values = ["10000", "50000", "100000", "500000", "1000000"]
rew_values = ["break-and-follow", "break", "follow"]
base_path = "testing/rounds/"
ds_all = pd.read_csv(base_path + "all.csv", sep=",")

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


def to_uppercase(arr):
    res = []
    for item in arr:
        res.append(item.upper())
    return res


def get_dataset(r=None):
    if r == None:
        return ds_all
    else:
        return ds_all[(ds_all.reward == r)]


def get_color(a):
    if a == "ppo":
        return c1
    elif a == "a2c":
        return c2
    return c3


def get_dataset_by_reward(a):
    if a == "break-and-follow":
        return ds_bf
    elif a == "break":
        return ds_b
    return ds_f


def generate_comparison_line():
    var_values = ["scores", "lives"]
    alg_values = ["ppo", "a2c", "dqn"]
    step_values = ["10K", "50K", "100K", "500K", "1M"]
    rew_values = ["break-and-follow", "break", "follow"]
    count = 1
    plt.figure(figsize=(12, 6))
    for v in var_values:
        for r in rew_values:
            for a in alg_values:
                d = get_dataset_by_reward(r)
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

    plt.savefig(
        "docs/img/all_combinations.pdf")


def generate_comparison_bars():
    scs = []
    lvs = []
    for r in rew_values:
        ds = get_dataset(r)
        scs.append(ds["score"].mean())
        lvs.append(ds["lives"].mean())
    plt.figure(figsize=(12, 6))
    plt.subplot(2, 3, 1)
    b1 = plt.bar(rew_values, scs, color=[c3])
    plt.bar_label(b1, np.around(scs, 2))
    plt.ylabel("score")
    plt.title('(a) rewards, score')
    plt.ylim(0, 100)

    plt.subplot(2, 3, 4)
    b1 = plt.bar(rew_values, lvs, color=[c3])
    plt.bar_label(b1, np.around(lvs, 2))
    plt.ylabel("lives")
    plt.title('(d) rewards, lives')
    plt.ylim(0, 4)

    ####
    scs = []
    lvs = []
    for a in alg_values:
        ds = get_dataset()
        ds = ds[(ds.algorithm.str.contains(a))]
        scs.append(ds["score"].mean())
        lvs.append(ds["lives"].mean())
    plt.subplot(2, 3, 2)
    b1 = plt.bar(to_uppercase(alg_values), scs, color=[c1, c2, c3])
    plt.bar_label(b1, np.around(scs, 2))
    plt.ylabel("score")
    plt.title('(b) algorithm, score')
    plt.ylim(0, 100)

    plt.subplot(2, 3, 5)
    b1 = plt.bar(to_uppercase(alg_values), lvs, color=[c1, c2, c3])
    plt.bar_label(b1, np.around(lvs, 2))
    plt.ylabel("lives")
    plt.title('(e) algorithm, lives')
    plt.ylim(0, 4)

    ####
    scs = []
    lvs = []
    for st in step_values:
        ds = get_dataset()
        ds = ds[(ds.algorithm.str.contains("_" + str(st)))]
        scs.append(ds["score"].mean())
        lvs.append(ds["lives"].mean())
    plt.subplot(2, 3, 3)
    b1 = plt.bar(step_values, scs, color=[c3])
    plt.bar_label(b1, np.around(scs, 2))
    plt.title("Average by # steps")
    plt.ylabel("score")
    plt.title('(c) steps, score')
    plt.ylim(0, 100)

    plt.subplot(2, 3, 6)
    b1 = plt.bar(step_values, lvs, color=[c3])
    plt.bar_label(b1, np.around(lvs, 2))
    plt.ylabel("lives")
    plt.title('(f) steps, lives')
    plt.tight_layout()
    plt.ylim(0, 4)
    plt.savefig("img/all_avgs.pdf")


def generate_top_scores_table():
    ds = get_dataset()
    tops = ds[(ds.score > 260) & (ds.lives >= 4)]
    print(tops.sort_values('score', ascending=False))

if __name__ == "__main__":
    generate_comparison_line()
    generate_comparison_bars()