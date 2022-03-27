from stable_baselines3 import DQN
from BreakoutAgent import BreakoutAgent

env = BreakoutAgent()
obs = env.reset()

model_name = "model_dqn_1000000"
model = DQN.load("models-break/" + model_name + ".zip")

for k in range(2000):
    action, _state = model.predict(obs, deterministic=True)
    obs, reward, done, info = env.step(action)
    env.render()
    print(info)
    if done:
        print("no more lives")
        break