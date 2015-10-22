# Source Files for Task5
### just copy paste code from here, no need to edit or change these files

The program gamestate.py does the following:

 * Assigns computer and player random colours - black always goes first
 * Takes user move by click
 * Auto generates computer move by chosing move that takes the most pieces
 * Allows the game to be saved when 'q' is pressed
 * Allows the game to be saved when 's' is pressed
 * Allows a new game to be started when 'n' is pressed

For Task 5 we only need the first three functionalities so just combine our current code from Task4 into the empty file in the root directory of this repo, along with the necessary functions from gamestate.py here.

The functions we'd need would be:

 * randomPlayer
 * calcTotal
 * bestMoveCalc
 * fillMoves (this function features in our current Task4 but there is a slight change on line 186 to allow the function to be used to search for the computer's moves too)
 * computerMove
 * coordBlack
 * coordWhite
 * userClickProcess (see the userClickProcess.py file for that function)

I've added an empty Task5.py file into the root directory so this folder can stay as a working reference, as we'll need the gamestate saving ability later in the semester.

The file userClickProcess.py is just there for reference of how the quit button was working with the userClickProcess function, as it's probably a good way of dealing with each user click.
