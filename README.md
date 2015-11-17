# Team075

### Nov 16 Updates
Bug noted: Kinda expected this, but if you click two valid moves quickly, it will play both moves, followed by giving the computer two moves. I guess this is because the main function is always waiting for a click. The only way around this would be to create a moveInProgress global variable that is turned to True when a userMove is triggered first and False when it ends, and then userClickProcess checks to make sure it is False before triggering userMove. 

I updated the masterReversi.py file with my most recent version. This has improved functions, an additional difficulty setting, and popup windows. We'll want to update the style and game saving to Greg's version soon but the functions in this version are pretty solid so it would be a good base to work from.

###Proof Of Concept reversi
I wrote the POC version so I could better understand the code and rewriting made it easier to implement new things. The code is mostly copy and pasted from masterReversi.py but I changed some variable names and logic to something that made sense to me. 

This version lets the user save and load games files and as such a place is needed to save and load from. That's what
the savedGames folder is for and it must be in the same directory as the .py file. The img folder is the same and it
contains some images that are used for the bgpic method, which is just a cosmetic change to the board.

This version will work for both Task 6 and Task 7 right now. However, I think a final redo of all the code would be a good idea before the final submission as I think some parts could be more elegant.

#### Misc Tasks
 * Anything else you think of!
