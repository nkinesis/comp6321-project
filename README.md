# Machine Learning (COMP 6321) Final Project
By Gabriel C. Ullmann, 2022

## Overview
In this project, I use three Reinforcement Learning algorithms (PPO, A2C, and DQN) to train an OpenAI Gym agent to play the game Breakout. Agents were trained using different combinations of algorithms, training steps, and reward functions to determine which one reaches the maximum average score and number of lives in the game.

## Project setup
On the root folder of this project, there is a requirements.txt file. Use pip to install all dependencies listed on it. You will need Python 3 to run the scripts correctly.

## Main scripts
You can execute the scripts from 1 to 6, in order. This way you can better understand how the game works, go through the training/testing process, and finally analyze the generated data.
1. Play Breakout as a human player, with no influence from agents.
1. Notebook: an overview on training/testing + getting metrics via Tensorboard. Script: training code for all combinations of parameters (algorithms and steps).
1. Testing code: running all combinations of agents on Breakout, recording results.
1. Testing code: running a "dummy" agent, our baseline.
1. Compute average scores/lives for each combination of parameters.
1. Generate plots from averages (as seen in the report).

You will also find in the root folder:
- breakout_agent: the OpenAI Gym environment class (the agent).
- unit_tests_game: unit tests for the game code.
- unit_tests_agent: unit tests for the agent code.

## Folders
A brief description of the contents of each folder in this project:
- Docs: contains generated plots and tables, project proposal, and final report.
- Game: contains the Breakout game code.
- Testing: contains data produced by the agents during the testing process.
    - Results: scores and number of lives for all test game sessions.
    - Rounds: original data from the three rounds of training/testing described in the report.
    - Tensorboard: original logs from Tensorboard, as described in the report.
- Training: model files are generated at the end of the training process.

## Contact
In case you have any questions, please contact me by e-mail: g_cavalh@live.concordia.ca
