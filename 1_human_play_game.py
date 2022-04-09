from game.breakout_game import BreakoutGame

""" All functions were written by Gabriel C. Ullmann, unless otherwise noted.

This script runs the game so you can play it directly, no agents playing yet. 
Use the keyboard arrows to move the bat left/right.
"""
game = BreakoutGame()
game.init_game()
while True:
    game.run_logic(-1)
    game.render()