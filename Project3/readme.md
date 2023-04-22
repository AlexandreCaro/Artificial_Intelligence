# PONTU
The present repository contains the Python code necessary for the LINFO1361 assignment 3.


## Setup

The game was implemented in **Python** and works with versions greater than or equal to **3.6+**. Just clone this repository or download the zip to get everything you need to run the game.

### Get Python and dependencies


You can download the **3.6+** version of Python [here](https://www.python.org/downloads/).
(Don't forget to add python to the path if you are on Windows)

Next, install the dependencies for the game by running the following command (note that you may need to replace ```pip``` by ```pip3``` if you have different versions of python).


```bash
pip install -r requirements.txt
```

### Run the code

You can run a match by executing the ```pontu_play.py``` script as follows (you may need to replace ```python``` by ```python3``` if you have different versions of python). A dummy AI agent is given in ```random_agent.py``` and a human agent (you!) is given in ```human_agent.py```.


**Usage:**

      python pontu_play.py -ai0 ai_0 -ai1 ai_1 -t 600 -f 0

      -ai0 
          path to the ai that will play as player 0
      -ai1 
           path to the ai that will play as player 1
      -t
           total number of seconds credited to each agent
      -f 
           indicates the player (0 or 1) that plays first; random otherwise
      -g   
           display GUI (true or false); by default true


**Examples:**

        python pontu_play.py -ai0 ai_0 -ai1 ai_1 -f 0 -g true

        python pontu_play.py -ai0 random_agent -ai1 human_agent -f 1 -g true

### Allowed time for each AI
The ```-t``` option allows you to specify the overall time (in seconds) allowed for all AI moves of each agent. If an agent exceeds his budget, he automatically loses the game.

**Example:**

         python main.py -ai0 ai_0 -ai1 ai_1 -t 120 -f 0 -g true

         python main.py -ai0 random_agent -ai1 random_agent -t 120 -f 1 -g false

### Pontu Rules
The goal of the game is to isolate all of your opponent's elves.

At each turn each player moves one of their elves from one circle/isle another by passing over a bridge and then removes one of the bridges, whichever they want, from the game board.

An elf can only move from one circle/isle to another if there is a bridge between the circles/isles.
Two elves (no matter if they have the same color or not) cannot be in the same circle/isle at the same time.
The last player who is able to move one of his elves wins the game.

In case one player cannot move any elves, because another elf is blocking the move, this player has not yet lost. He must only remove a bridge from the board without moving any elves. 

### Human Agent
The ```human_agent.py``` gives you the possibility to play your own games against one of your agent or one of your friends.

To play a turn, you first have to click on a valid elf/pawn, then click on a valid destination circle/isle and finally click on a valid bridge to remove. The state of the board will be updated once the three actions are completed, not before!

### For Windows Users :(
The game was implemented to run on a Unix machine. If you try to launch a game on Windows, you will have errors!

However by commenting the lines of code 99, 100 and 105 of the ```pontu_tools.py``` file, you should be able to run Pontu Windows. However, the game will not stop if a player has exceeded his time budget.

**Example:**

        """
        Get an action from player with a timeout.
        """
        def get_action_timed(player, state, last_action, time_left):
            #signal.signal(signal.SIGALRM, handle_timeout)      <----------------
            #signal.setitimer(signal.ITIMER_REAL, time_left)    <----------------
            exe_time = time.time()
            try:
                action = player.get_action(state, last_action, time_left)
            finally:
                #signal.setitimer(signal.ITIMER_REAL, 0)        <----------------
                exe_time = time.time() - exe_time
            return action, exe_time
