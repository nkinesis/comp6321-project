from game.breakout_game import BreakoutGame

game = BreakoutGame()
game.init_game()
while True:
    game.run_logic(-1)
    game.render()