import random
from state import State
from copy import deepcopy


DIRECTIONS = ['WEST','NORTH','EAST','SOUTH']


class PontuState(State):

    def __init__(self, size = 5):
        self.cur_player = random.randint(0, 1)
        self.winner = None
        self.timeout_player = None
        self.invalid_player = None
        self.size = size

        # Indicates the position of the pawns: self.cur_pos[i][j] is the (x,y) position of jth pawn of player i
        # The origin (0,0) position corresponds to the top left island (North-east)
        self.cur_pos = [[(i,1) for i in range(1,self.size-1)], [(i,3) for i in range(1,self.size-1)]]

        # Indicates the blocked pawns: self.blocked[i][j] is True if the jth pawn of player i has no adjacent bridge
        self.blocked = [[False for i in range(self.size-2)], [False for i in range(self.size-2)]]

        # Indicates if the horizontal bridges are still present:
        # self.h_bridges is a 5x4 boolean matrix represented by a list of lists of boolean. Its initial form is:
         # [[True, True, True, True],
         #  [True, True, True, True],
         #  [True, True, True, True],
         #  [True, True, True, True],
         #  [True, True, True, True]]
        # self.h_bridges[y][x] is True if the horizontal bridge on position (x,y) is on the board
        # self.h_bridges[0][0] corresponds to the leftmost horizontal bridge of the top line
        self.h_bridges = [[True for i in range(self.size-1)] for j in range(self.size)]

        # Indicates if the vertical bridges are still present:
        # self.v_bridges is a 4x5 boolean matrix represented by a list of lists of boolean. Its initial form is:
        # [[True, True, True, True, True],
        #  [True, True, True, True, True],
        #  [True, True, True, True, True],
        #  [True, True, True, True, True]]
        # self.v_bridges[y][x] is True if the vertical bridge on position (x,y) is on the board
        # self.v_bridges[0][0] corresponds to the upmost vertical bridge of the left column
        self.v_bridges = [[True for i in range(self.size)] for j in range(self.size-1)]

        # Contains all the previous moves
        self.history = []

        # The number of turns already played
        self.turns = 0

    def __eq__(self, other):
        return self.cur_player == other.cur_player and self.cur_pos == other.cur_pos

    def set_timed_out(self, player):
        self.timeout_player = player
        self.winner = 1 - player

    def set_invalid_action(self, player):
        self.invalid_player = player
        self.winner = 1 - player

    """
    Returns the position of the requested pawn ((x, y) position on the board)
    """

    def get_pawn_position(self, player, pawn):
        return self.cur_pos[player][pawn]

    """
    Returns whether the pawn is blocked
    """

    def is_pawn_blocked(self, player, pawn):
        return self.blocked[player][pawn]

    """
    Return a deep copy of this state.
    """

    def copy(self):
        cp = PontuState()
        cp.cur_player = self.cur_player
        cp.winner = self.winner
        cp.timeout_player = self.timeout_player
        cp.invalid_player = self.invalid_player
        cp.cur_pos = deepcopy(self.cur_pos)
        cp.blocked = deepcopy(self.blocked)
        cp.h_bridges = deepcopy(self.h_bridges)
        cp.v_bridges = deepcopy(self.v_bridges)
        cp.history = deepcopy(self.history)
        cp.turns = self.turns
        return cp

    """
    Return true if and only if the game is over (game ended, player timed out or made invalid move).
    """

    def game_over(self):
        if self.winner != None:
            return True
        return self.game_over_check()

    """
    Checks if a player succeeded to win the game, i.e. move 4 pawns to the other side and back again.
    """

    def game_over_check(self):
        if sum(self.blocked[0]) >= 3:
            if sum(self.blocked[1]) >= 3:
                self.winner = -1 # means the game is a tie
            else:
                self.winner = 1
            return True
        elif sum(self.blocked[1]) >= 3:
            self.winner = 0
            return True
        else:
            return False

    """
    Return the index of the current player.
    """

    def get_cur_player(self):
        return self.cur_player

    """
    Checks if a given action is valid.
    An action is a tuple of the form (pawn_id, direction, type_of_bridge, bridge_x, bridge_y) where:
     - pawn_id : integer of value 0, 1 or 2 indicating the id of the pawn that will move during the action
     - direction : string which must take one of the following values "EAST", "NORTH", "WEST" or "SOUTH" indicating in which
                   direction the pawn will move
     - type_of_bridge : string equal to "h" or "v" indicating if the bridge that will be removed is a horizontal or
                        vertical bridge
     - bridge_x : integer indicating the x (absciss) position of the bridge (from 0 to 3 for horizontal bridges and 
                  from 0 to 4 for vertical bridges)
     - bridge_y : integer indicating the y (ordinate) position of the bridge (from 0 to 4 for horizontal bridges and 
                  from 0 to 3 for vertical bridges)
    
    If the pawns can't move because they are blocked by other pawns but the game isn't over, then the valid actions 
    only consist on removing one bridge. In this case pawn_id and direction will both be equal to None.
    """

    def is_action_valid(self, action):
        actions = self.get_current_player_actions()
        return action in actions

    """
    Get all the actions that the current player can perform.
    The structure of an action is explain in the is_action_valid method description.
    """

    def get_current_player_actions(self):
        actions = []
        for i in range(self.size-2): # for each pawn
            if not self.blocked[self.cur_player][i]: # if the pawn is not blocked
                    dirs = self.move_dir(self.cur_player,i)
                    for dir in dirs: # for each direction the pawn can move towards
                        for y in range(len(self.h_bridges)): # for each y position of horizontal bridges
                            for x in range(len(self.h_bridges[y])): # for each x position of the horizontal bridges
                                if self.h_bridges[y][x]: # if the horizontal bridge is present
                                    actions.append((i,dir,'h',x,y)) # add the corresponding action to the list
                        for y in range(len(self.v_bridges)): # for each y position of vertical bridges
                            for x in range(len(self.v_bridges[y])): # for each x position of the vertical bridges
                                if self.v_bridges[y][x]: # if the vertical bridge is present
                                    actions.append((i,dir,'v',x,y)) # add the corresponding action to the list

        # if there is no action => the pawns can't move but there is still at least one pawn with an adjacent bridge
        if len(actions) == 0:
            # then the valid actions consist only on the removal of one bridge
            for y in range(len(self.h_bridges)):
                for x in range(len(self.h_bridges[y])):
                    if self.h_bridges[y][x]:
                        actions.append((None, None, 'h', x, y))
            for y in range(len(self.v_bridges)):
                for x in range(len(self.v_bridges[y])):
                    if self.v_bridges[y][x]:
                        actions.append((None, None, 'v', x, y))
        return actions

    """
    Check if a pawn is blocked.
     - player is the id of the pawn's player
     - pawn is the id of the pawn
    """
    def pawn_blocked_check(self,player,pawn):
        adj_bridges = self.adj_bridges(player, pawn)
        if sum(adj_bridges.values()) == 0:
            self.blocked[player][pawn] = True

    """
    Check in which direction a pawn can move
     - player is the id of the pawn's player
     - pawn is the id of the pawn
     It returns a list of the directions ('WEST','NORTH','EAST','SOUTH') it can move towards
    """
    def move_dir(self,player,pawn):
        dirs = []
        adj_bridges = self.adj_bridges(player, pawn)
        adj_pawns = self.adj_pawns(player, pawn)
        for dir in DIRECTIONS:
            if adj_bridges[dir] and not adj_pawns[dir]:
                dirs.append(dir)
        return dirs


    """
    Check the for presence of bridges adjacent to a specific pawn
     - player is the id of the pawn's player
     - pawn is the id of the pawn
    It returns a dictionary with 4 entries : "EAST", "NORTH", "WEST" or "SOUTH".
    The associated value is True if there is a bridge in this direction or False if there is none.
    """
    def adj_bridges(self,player,pawn):
        pos = self.get_pawn_position(player,pawn)
        return self.adj_bridges_pos(pos)

    """
        Check the for presence of bridges adjacent to a specific isle/position
         - pos is the tuple (x,y) representing the coordinate of the isle
        It returns a dictionary with 4 entries : "EAST", "NORTH", "WEST" or "SOUTH".
        The associated value is True if there is a bridge in this direction or False if there is none.
        """

    def adj_bridges_pos(self, pos):
        bridges = {}
        # Check west bridge
        if pos[0] >= 1:
            bridges['WEST'] = self.h_bridges[pos[1]][pos[0] - 1]
        else:
            bridges['WEST'] = False
        # Check north bridge
        if pos[1] >= 1:
            bridges['NORTH'] = self.v_bridges[pos[1] - 1][pos[0]]
        else:
            bridges['NORTH'] = False
        # Check east bridge
        if pos[0] < self.size - 1:
            bridges['EAST'] = self.h_bridges[pos[1]][pos[0]]
        else:
            bridges['EAST'] = False
        # Check south bridge
        if pos[1] < self.size - 1:
            bridges['SOUTH'] = self.v_bridges[pos[1]][pos[0]]
        else:
            bridges['SOUTH'] = False
        return bridges

    """
    Check the for presence of pawns adjacent to a specific pawn
     - player is the id of the pawn's player
     - pawn is the id of the pawn
    It returns a dictionary with 4 entries : "EAST", "NORTH", "WEST" or "SOUTH".
    The associated value is True if there is a pawn in this direction or False if there is none.
    """

    def adj_pawns(self, player, pawn):
        pos = self.get_pawn_position(player,pawn)
        return self.adj_pawns_pos(pos)

    """
        Check the for presence of pawns adjacent to a specific isle/position
         - pos is the tuple (x,y) representing the coordinate of the isle
        It returns a dictionary with 4 entries : "EAST", "NORTH", "WEST" or "SOUTH".
        The associated value is True if there is a pawn in this direction or False if there is none.
        """

    def adj_pawns_pos(self, pos):
        pawns = {}
        # Check west island
        west_pawn = False
        if pos[0] >= 1:
            for player in self.cur_pos:
                for (x, y) in player:
                    if pos == (x + 1, y):
                        west_pawn = True
        pawns['WEST'] = west_pawn
        # Check north island
        north_pawn = False
        if pos[1] >= 1:
            for player in self.cur_pos:
                for (x, y) in player:
                    if pos == (x, y + 1):
                        north_pawn = True
        pawns['NORTH'] = north_pawn
        # Check east island
        east_pawn = False
        if pos[0] < self.size - 1:
            for player in self.cur_pos:
                for (x, y) in player:
                    if pos == (x - 1, y):
                        east_pawn = True
        pawns['EAST'] = east_pawn
        # Check south island
        south_pawn = False
        if pos[1] < self.size - 1:
            for player in self.cur_pos:
                for (x, y) in player:
                    if pos == (x, y - 1):
                        south_pawn = True
        pawns['SOUTH'] = south_pawn
        return pawns

    """
    Applies a given action to this state. It assume that the actions is
    valid. This must be checked with is_action_valid.
     - action is the action to be applied to the state
    """

    def apply_action(self, action):
        (pawn, d, b, x_b, y_b) = action
        if action[0] is not None:
            (x,y) = self.cur_pos[self.cur_player][pawn]
            if d == 'WEST':
                self.cur_pos[self.cur_player][pawn] = (x-1,y)
            elif d == 'NORTH':
                self.cur_pos[self.cur_player][pawn] = (x, y-1)
            elif d == 'EAST':
                self.cur_pos[self.cur_player][pawn] = (x+1, y)
            elif d == 'SOUTH':
                self.cur_pos[self.cur_player][pawn] = (x, y+1)
        if b == 'h':
            self.h_bridges[y_b][x_b] = False
        elif b == 'v':
            self.v_bridges[y_b][x_b] = False

        # check if the action results in new blocked pawns
        for i in range(2):
            for j in range(self.size-2):
                if not self.blocked[i][j]:
                    self.pawn_blocked_check(i,j)

        self.turns += 1
        self.history.append(action)
        self.cur_player = 1 - self.cur_player

    """
    Return the scores of each players.
    """

    def get_scores(self):
        if self.winner is None or self.winner == -1:
            return (0, 0)
        elif self.winner == 0:
            return (1, 0)
        return (0, 1)

    """
    Get the winner of the game. Call only if the game is over.
    """

    def get_winner(self):
        return self.winner

    """
    Return the information about the state that is given to students.
    Usually they have to implement their own state class.
    """

    def get_state_data(self):
        pass
