### Instructions On Usage ###

My program utilises two libraries, glob and time, both of which are in the default library.
Therefore no seperate installs are required.

My program will automatically perform a DF and greedy search on any mazes you place within the folder called mazes.
The mazes folder must exist in the same directory as AICA.py.

The results of each search will be output to a folder called results.
Again please ensure that there is a folder called results placed within the same directory as AICA.py.


Once you have placed all your mazes in the folder you can run the program with the command:

python AICA.py

Then follow the commands on the terminal.


### Maze Structure ###

Mazes must be made of:
'-' to represent a navigable space
'#' to represent a wall
There can be spaces between symbols

There must only be one '-' on the top and bottom rows as my program will automatically detect a start and goal point.
Example:
VALID           INVALID
##-####         ##-##-#
#----##         #----## 
#-##--#         #-##--#
#####-#         #-###-#