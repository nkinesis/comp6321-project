from datetime import datetime
from breakout_agent import BreakoutAgent

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
results_path = "testing/results"
results_filename = "score_" + timestamp + ".csv"

with open(results_path + "/" + results_filename, "a") as file:
  file.write("algorithm,iteration,score,lives,timestamp\n")

env = BreakoutAgent()
episodes = 2000
results = []
for i in range(0, 60):
    obs = env.reset()
    for episode in range(episodes):
        random_action = env.action_space.sample()
        obs, reward, done, info = env.step(random_action)
        env.render()
        if done:
            print("No more lives, game over!")
            break

        with open(results_path + "/" + results_filename, "a") as file:
            p1 = "dummy"
            p2 = str(i)
            p3 = str(info["score"])
            p4 = str(info["lives"])
            p5 = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            file.write(p1 + "," + p2 + "," + p3 + "," + p4 + "," + p5 + "\n")