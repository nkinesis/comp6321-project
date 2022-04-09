import time
from datetime import datetime
from stable_baselines3 import PPO
from stable_baselines3 import A2C
from stable_baselines3 import DQN
from breakout_agent import BreakoutAgent

""" All functions were written by Gabriel C. Ullmann, unless otherwise noted.

This script will test every agent trained during the training process.
It reads all model files in the folder testing/results.
By default it will run just 1 game session for each model.
You can run several sessions by changing the n_sessions variable.

If you want to speed up the process, you can change the code below to run with just one combination. For example:

list_algs = [PPO]
list_algs_names = ["ppo"]
list_steps = [10000]
"""
n_sessions = 1
list_algs = [PPO, A2C, DQN]
list_algs_names = ["ppo", "a2c", "dqn"]
list_steps = [10000, 50000, 100000, 500000, 1000000]
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
results_path = "testing/results"
results_filename = "score_" + timestamp + ".csv"

with open(results_path + "/" + results_filename, "a") as file:
    file.write("algorithm,reward,iteration,score,lives,timestamp\n")

env = BreakoutAgent()
obs = env.reset()
reward_case = "break-follow"

""" Iterate over all combinations, test, save results """
for i in range(0, len(list_algs_names)):
    for j in range(0, len(list_steps)):
        model_name = "model_" + list_algs_names[i] + "_" + str(list_steps[j])
        model = list_algs[i].load("training/" + model_name + ".zip")
        print("now:" + model_name)
        time.sleep(1)
        for k in range(0, n_sessions):
            obs = env.reset()
            for l in range(2000):
                action, _state = model.predict(obs, deterministic=True)
                obs, reward, done, info = env.step(action)
                env.render()
                print(info)
                if done:
                    print("No more lives, game over!")
                    break

            with open(results_path + "/" + results_filename, "a") as file:
                p1 = model_name + " - " + reward_case
                p2 = reward_case
                p3 = str(k)
                p4 = str(info["score"])
                p5 = str(info["lives"])
                p6 = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                file.write(
                    p1 +
                    "," +
                    p2 +
                    "," +
                    p3 +
                    "," +
                    p4 +
                    "," +
                    p5 +
                    "," +
                    p6 +
                    "\n")
