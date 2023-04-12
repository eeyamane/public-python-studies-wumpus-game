# public-python-studies-wumpus-game
Studies of Python with Wumpus game

About the Wumpus game:

The Wumpus game is a classic text-based adventure game that was first developed in the 1970s. In the game, the player takes on the role of a Adventurer who is trying to find a Treasure and meanwhile, can track down and kill a dangerous beast known as the Wumpus, which is lurking in a network of caves.

The game is played on a grid-like map, where each room is connected to other rooms by tunnels. The player must navigate through the cave system, avoiding hazards such as Bottomless Pits that will kill the Adventurer, and giant Bats that will take the Adventurer to some random room, while searching for the Treasure and/or the Wumpus.

The Wumpus is located in a single room on the map, which the player can identify by the smell of its foul breath at adjacent rooms. The Pits can be identified by a breeze they generate at adjancent rooms. The player must use their wits to find a way to find the Treasure and/or get close enough to the Wumpus to take it down with their arrows, without being caught in one of its traps.

The Wumpus game is often used as a teaching tool in AI courses to introduce students to concepts such as search algorithms, logic-based reasoning, and decision-making under uncertainty.

About the code:

As I started to learn Python, I just wanted to create something. Remembering the old days of one of my AI courses, I realized the Wumpus game could be something fun to explore. The results are here.

I divided the work in three modules:

- wumpus_game_model: some basic classes used to model the problem. Besides, it includes some simple models with the "engines" to run the game in text mode. Although these "engines" don't work now (because after using them to test things, I changed the directory structure), the old cold is included in directory wumpus-teste

- wumpus_world_builder: some simple GUI to design an instance of the game. You can save a file with the game and load it in the other module. The file uses a simple JSON format. You can run the program with command (from outside the directory): 
py -m wumpus_world_builder.gui-world-builder

- wumpus_game_grided_gui: it contains a GUI to play the game, along with image files used. You can run the program with command (from outside the directory): 
py -m wumpus_game_grided_gui.wumpus-game-gui

- wumpus-teste: this is not a module, but an older version of files in wumpus_game_model. It also contains a script to run a text-based version of the game. You can run with the command:
cd wumpus-teste
py wumpus_run.py

Original image files are from https://www.flaticon.com/free-icons. Some images where changed, but you can see I am not a designer. Original links are in .py file.

GUI uses PySimpleGUI (https://www.pysimplegui.org/)
