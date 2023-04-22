from agent import AlphaBetaAgent
from pontu_state import *
import minimax
import copy
import math


"""
Agent skeleton. Fill in the gaps.
"""
class MyAgent(AlphaBetaAgent):
  def __init__(self):
    self.dept = None
  def get_name(self):
    return 'maxime agent'

  """
  This is the skeleton of an agent to play the Tak game.
  """
  def get_action(self, state, last_action, time_left):
    self.last_action = last_action
    self.time_left = time_left
    self.dept = self.dept_choose(state)
    return minimax.search(state, self)

  """
  The successors function must return (or yield) a list of
  pairs (a, s) in which a is the action played to reach the
  state s.
  """
  def successors(self, state):
    actions = state.get_current_player_actions()
    for action in actions:
        
        act_state = copy.deepcopy(state)
        act_state.apply_action(action)
        yield action, act_state

    
  """
  The cutoff function returns true if the alpha-beta/minimax
  search has to stop and false otherwise.
  """
  def cutoff(self, state, depth):
    if depth >= self.dept or state.game_over():
       return True
    else:
       return False

  """
  The evaluate function must return an integer value
  representing the utility function of the board.
  """
  def evaluate(self, state: PontuState):
    score = 0
    enemie = 1-self.id
    for pawn in range(3):
        x,y = state.cur_pos[enemie][pawn]
        ajd = state.adj_bridges_pos((x,y))
        for key, value in ajd.items():
          if not value:
            score +=1
            position = (x,y)
          else:
            if key == "WEST":
              position = (x-1,y)
            if key == "EAST":
              position = (x+1,y)
            if key == "NORTH":
              position = (x,y-1)
            if key == "SOUTH":
              position = (x,y+1)

            aj2 = state.adj_bridges_pos(position)
            for j in aj2.values():
              if j:
                score -=0.5 
    for pawn in range(3):
        x,y = state.cur_pos[self.id][pawn]
        ajd = state.adj_bridges_pos((x,y))
        for key, value in ajd.items():
          if not value:
            score -=1
            position = (x,y)
          else:
            if key == "WEST":
              position = (x-1,y)
            if key == "EAST":
              position = (x+1,y)
            if key == "NORTH":
              position = (x,y-1)
            if key == "SOUTH":
              position = (x,y+1)
            aj2 = state.adj_bridges_pos(position)

            for j in aj2.values():
              if j:
                score +=0.5 
    return score

  def dept_choose(self,state):
    num =0
    for pawn in range(3):
      ajd = state.adj_bridges(self.id,pawn)
      for key, value in ajd.items():
        if value:
          num +=1
    
    count = 0
    for i in state.h_bridges:
      count += i.count(True)
    prof = num * count +1
    if prof <= 1:
      prof = 2
    return int(math.log(self.time_left*10000,prof))