from agent import AlphaBetaAgent
import minimax

"""
Agent skeleton. Fill in the gaps.
"""
class MyAgent(AlphaBetaAgent):

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
    successors = []

    for action in state.get_current_player_actions():
      copied_state = state.copy()

      if copied_state.is_action_valid(action):
        copied_state.apply_action(action)
        successors.append((action, copied_state))

    print(len(successors))

    return successors

  """
  The cutoff function returns true if the alpha-beta/minimax
  search has to stop and false otherwise.
  """
  def cutoff(self, state, depth):
    return depth >= 1 or state.game_over()

  """
  The evaluate function must return an integer value
  representing the utility function of the board.
  """
  def evaluate(self, state):
    evaluation = 0
    opponent_player = 1 - self.id

    for opponent_pawn in range(len(state.cur_pos[opponent_player])):
      for value in state.adj_bridges(opponent_player, opponent_pawn).values():
        if not value:
          evaluation += 1

    for player_pawn in range(len(state.cur_pos[self.id])):
      for value in state.adj_bridges(self.id, player_pawn).values():
        if not value:
          evaluation -= 1

    return evaluation