from agent import AlphaBetaAgent
from pontu_state import *
import minimax
import copy

"""
Agent skeleton. Fill in the gaps.
"""
class MyAgent(AlphaBetaAgent):

  def get_name(self):
    return 'smart_agent1.0'

  """
  This is the skeleton of an agent to play the Tak game.
  """
  def get_action(self, state, last_action, time_left):
    self.last_action = last_action
    self.time_left = time_left

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
    if depth >= 1 or state.game_over():
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
    for pawn in range(len(state.cur_pos[1])):
        ajd = state.adj_bridges(enemie,pawn)
        for i in ajd.values():
            if not i:
              score +=1
    return score
              


"""
1. CARACTERISTIQUES
    - position des ponts: représente la position du noeud à qui appartients les 2 ponts associé à cette position ( le ponts SUD et EST)
    - orientation des ponts: dit si le pont est 'v' verticale ou 'h' horizontale ps:(dans l'exemple précédent, 'v' = SUD et 'h' = EST)
2. VARIABLES
    - position des pions: liste avec en position 0:ensemble de tuple représentant le j1 1:ensemble de tuple représentant le j2  exemple :[[(1, 1), (2, 0), (3, 1)], [(1, 3), (2, 3), (3, 3)]]
    - représentation des ponts: matrice de bool représentant les positions des ponts et si ils sont activé ou non
            [[True, True, True, True],
            [True, True, True, True],
            [True, True, True, True],
            [True, True, True, True],
            [True, True, True, True]]
    -action représenté par une liste (numéro du pion, direction de l'action, sur la position quel est l'orientation du pont à supprimer, (position x du pont,position y du pont))  exemple: (0, 'SOUTH', 'v', 2, 1) 
3.FONCTIONS
    
"""