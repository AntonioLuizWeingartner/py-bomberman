# PY-BOMBERMAN
# ABOUT THE PROJECT :clipboard:
This game was developed at the 2nd semester of my graduation. It uses PyGame for rendering and an Entity-Component organization for the game's logic. My Entity-Component organization isn't an entity component system (ECS). In my implementation, components are containers for both logic and data, so it can't be categorized as an entity component system. Also, my logic system isn't cache-friendly so it can't handle a large amount of entities.
<br/>
# ABOUT THE GAME 💣
This game was inspired by the original bomberman game that was launched back in 1983 by **Hudson Soft**. The mechanics of my game are similar to the original bomberman, but the goal is different: here the player must eliminate as much enemies as possible before it eventually gets hit by the computer controlled enemies.
<br/>
# DETAILS ABOUT THE GAME'S AI :robot:
The game's AI uses the __A* pathfinding algorithm__, **Flood Fill algorithm** and a **state machine** to define it's behaviour.
<br/>
# HOW TO PLAY 🎮
First, download or clone this repository to your machine. This game should run on any machine that supports python >= 3.7.x.<br/>
After downloading the repository, run the file game.py with your interpreter and the game should be launched. If everything went right, you should now be seeing an interface with two light-blue buttons. Click the button with the text *'PLAY'* to start the game.
<br />
### CONTROLS
The controls are fairly simple: Use your keyboard arrow keys to move around the map and the space bar to place bombs. Black blocks are indestructible and gray blocks are destructible.

# SCREENSHOTS




