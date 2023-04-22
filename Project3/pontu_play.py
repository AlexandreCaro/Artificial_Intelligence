from pontu_tools import *
import argparse

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument("-ai0", help="path to the ai that will play as player 0")
  parser.add_argument("-ai1", help="path to the ai that will play as player 1")
  parser.add_argument("-t", help="time out: total number of seconds credited to each AI player")
  parser.add_argument("-f", help="indicates the player (0 or 1) that plays first; random otherwise")
  parser.add_argument("-g", help="display GUI (true or false); by default true")
  args = parser.parse_args()

  agent0 = args.ai0 if args.ai0 != None else "human_agent"
  agent1 = args.ai1 if args.ai1 != None else "human_agent"
  time_out = float(args.t) if args.t != None else 900.0
  first = int(args.f) if args.f == '1' or args.f == '0' else None
  display_gui = args.g == None or args.g.lower() == "true"

  if (agent0 == "human_agent" or agent1 == "human_agent") and display_gui == False:
    print('The GUI must be diplayed if a human agent is playing')
    display_gui = True

  initial_state = PontuState()
  if first is not None:
    initial_state.cur_player = first
  agent0 = getattr(__import__(agent0), 'MyAgent')()
  agent0.set_id(0)
  agent1 = getattr(__import__(agent1), 'MyAgent')()
  agent1.set_id(1)
  res = play_game(initial_state, [agent0.get_name(), agent1.get_name()], [agent0, agent1], time_out, display_gui)
  print(res)
