# Team075

### Nov 30 Updates
The reversiPOCmagic.py board coordinates have been changed to fit the feedback of the TA and Rob. The only way to scale the board to centre is to have 0,0 as the centre coordinates, so the board has been changed to reflect that. Our TA also seemed confused at our use of world coordinates which were integral to our previous setup, and I think altering the natural turtle setup would have probably been deemed 'unnecessary' by markers, especially when scaling issues were run into. Overall, it didn't take too much editing and only the coordinates were altered, not any of the main functions.

In addition to this, all coordinates have now been defined in terms of PIECE_SIZE so when changing that constant, the board now scales nicely. We could also make this an in-game option - change game size, which would just change the global variable PIECE_SIZE, and everything would scale.

### To Do:
 * Main project description/documentation
 * New game button
 * Overwrite previously saved game, with check ('do you want to overwrite?')
 * I might look into setting up the hints functionality

#### Misc Tasks
 * Looking through code, checking for inconsistencies etc.
 * Anything else you think of!
