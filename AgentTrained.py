import time
from datetime import datetime
from stable_baselines3 import PPO
from stable_baselines3 import A2C
from stable_baselines3 import DQN
from BreakoutAgent import BreakoutAgent

list_algs = [PPO, A2C, DQN]
list_algs_names = ["ppo", "a2c", "dqn"]
list_steps = [10000, 50000, 100000, 500000, 1000000]

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
with open("scores/score_" + timestamp + ".csv", "a") as file:
  file.write("algorithm,steps,score,lives,timestamp\n")

env = BreakoutAgent()
obs = env.reset()
reward_case = "reward=break-follow"

# for each model and steps
# test 10 times for 30 seconds (2000 steps)

for i in range(0, len(list_algs_names)):
  for j in range(0, len(list_steps)):
    model_name = "model_" + list_algs_names[i] + "_" + str(list_steps[j])
    model = list_algs[i].load("models-break-follow/" + model_name + ".zip")
    print("now:" + model_name)
    time.sleep(1)
    for k in range(0, 10):
      obs = env.reset()
      for l in range(2000):
        action, _state = model.predict(obs, deterministic=True)
        obs, reward, done, info = env.step(action)
        env.render()
        print(info)
        if done:
          print("no more lives")
          break

      with open("scores/score_" + timestamp + ".csv", "a") as file:
        p1 = model_name + " - " + reward_case
        p2 = str(k)
        p3 = str(info["score"])
        p4 = str(info["lives"])
        p5 = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file.write(p1 + "," + p2 + "," + p3 + "," + p4 + "," + p5 + "\n")
