from datetime import datetime
from stable_baselines3 import PPO
from stable_baselines3 import A2C
from stable_baselines3 import DQN
from breakout_agent import BreakoutAgent

""" All functions were written by Gabriel C. Ullmann, unless otherwise noted.

This script will train agents with all combinations of algorithms and steps.
The rewards are defined in the BreakoutAgent (default is break-and-follow, the optimal one).
If you want to speed up the process, you can change the code below to run with just one combination. For example:

list_algs = [PPO]
list_algs_names = ["ppo"]
list_steps = [10000]
"""
list_algs = [PPO, A2C, DQN]
list_algs_names = ["ppo", "a2c", "dqn"]
list_steps = [10000, 50000, 100000, 500000, 1000000]

""" Path to test result files """
results_path = "testing/results"
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
results_filename = "score_" + timestamp + ".csv"

with open(results_path + "/" + results_filename, "a") as file:
    file.write("algorithm,steps,score,lives,timestamp\n")

""" Iterate over all combinations, train, test for 1 session, save results """
for i in range(0, len(list_algs)):
    for j in range(0, len(list_steps)):
        model_filename = "_" + list_algs_names[i] + "_" + str(list_steps[j])

        env = BreakoutAgent()
        model = list_algs[i]('MlpPolicy', env, verbose=1)
        model.learn(total_timesteps=list_steps[j])
        obs = env.reset()
        model.save("training/model" + model_filename)

        for k in range(2000):
            action, _state = model.predict(obs, deterministic=True)
            obs, reward, done, info = env.step(action)
            env.render()
            print(info)
            if done:
                print("No more lives, game over!")
                break

        with open(results_path + "/" + results_filename, "a") as file:
            p1 = list_algs_names[i]
            p2 = str(list_steps[j])
            p3 = str(info["score"])
            p4 = str(info["lives"])
            p5 = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            file.write(p1 + "," + p2 + "," + p3 + "," + p4 + "," + p5 + "\n")
