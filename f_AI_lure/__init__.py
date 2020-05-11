# Note:
# The class defined within this module with the name 'Player' is the
# class we will test when assessing your project.
# You can define your player class inside this file, or, as in the
# example import below, you can define it in another file and import
# it into this module with the name 'Player':

#from your_team_name.player import Player as Player
from f_AI_lure.player import Player as Player
import tracemalloc

if __name__ == "__main__":
    
    tracemalloc.start()
    
    newPlayer = Player('white')
    actions = newPlayer.action()
    newPlayer.update('white', actions)
    print(actions)
    
    current, peak = tracemalloc.get_traced_memory()
    print(f"Current memory usage is {current / 10**6}MB; Peak was {peak / 10**6}MB")
    tracemalloc.stop()
    