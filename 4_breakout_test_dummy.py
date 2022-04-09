from datetime import datetime
from breakout_agent import BreakoutAgent

""" All functions were written by Gabriel C. Ullmann, unless otherwise noted.

This script will run a 'dummy' agent to play the game.
This kind of agent only tries random actions, it has not been trained and it does not learn.
The 'dummy' is useful as a baseline. It is expected that any adequately trained agent will play better than a random one.
By default it will run just 1 game session. You can run several sessions by changing the n_sessions variable.
"""
n_sessions = 1
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
results_path = "testing/results"
results_filename = "score_" + timestamp + ".csv"

with open(results_path + "/" + results_filename, "a") as file:
  file.write("algorithm,iteration,score,lives,timestamp\n")

env = BreakoutAgent()
steps = 2000
results = []
for i in range(0, n_sessions):
    obs = env.reset()
    for step in range(steps):
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