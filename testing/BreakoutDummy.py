from datetime import datetime
from BreakoutAgentBatch import BreakoutAgent

env = BreakoutAgent()
episodes = 2000
results = []
for i in range(0, 10):
    obs = env.reset()
    for episode in range(episodes):
        random_action = env.action_space.sample()
        print("action",random_action)
        obs, reward, done, info = env.step(random_action)
        print('reward',reward)
        print("obs", obs)
        env.render()
        if done:
            print("no more lives")
            break
    results.append([info, datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
    print(results)
print(results)