import pygame
from agent import Agent

class MyAgent(Agent):
	def __init__(self):
		self.clock = pygame.time.Clock()
	
	def get_action(self, state, last_action, time_left):
		select_pawn = False
		pawn_id = None
		moved_pawn = False
		dir = None
		select_bridge = False
		action = None
		actions = state.get_current_player_actions()

		if actions[0][0] is None:
			select_pawn = True
			moved_pawn = True
		
		while not select_pawn:
			self.clock.tick(30)
			for event in pygame.event.get():
				if event.type == pygame.MOUSEBUTTONUP:
					pos = pygame.mouse.get_pos()
					x = int(pos[0]/50)
					y = int(pos[1]/50)
					if x < state.size * 2 - 1 and y < state.size * 2 - 1:
						if x % 2 == 0 and y % 2 ==0:
							x = x/2
							y = y/2
							for i in range(state.size-2):
								if (x,y) == state.get_pawn_position(state.cur_player,i):
									select_pawn = True
									pawn_id = i

				if event.type == pygame.QUIT:
					#pygame.quit()
					return ('rage-quit', None, None, None, None)

		while not moved_pawn:
			self.clock.tick(30)
			for event in pygame.event.get():
				if event.type == pygame.MOUSEBUTTONUP:
					pos = pygame.mouse.get_pos()
					x = int(pos[0]/50)
					y = int(pos[1]/50)
					if x < state.size * 2 - 1 and y < state.size * 2 - 1:
						if x % 2 == 0 and y % 2 ==0:
							x = x/2
							y = y/2
							(X,Y) = state.get_pawn_position(state.cur_player, pawn_id)
							adj_bridges = state.adj_bridges(state.cur_player, pawn_id)
							adj_pawns = state.adj_pawns(state.cur_player, pawn_id)
							if x == X - 1 and y == Y and adj_bridges['WEST'] and not adj_pawns['WEST']:
								moved_pawn = True
								dir = 'WEST'
							elif x == X and y == Y - 1 and adj_bridges['NORTH'] and not adj_pawns['NORTH']:
								moved_pawn = True
								dir = 'NORTH'
							elif x == X + 1 and y == Y and adj_bridges['EAST'] and not adj_pawns['EAST']:
								moved_pawn = True
								dir = 'EAST'
							elif x == X and y == Y + 1 and adj_bridges['SOUTH'] and not adj_pawns['SOUTH']:
								moved_pawn = True
								dir = 'SOUTH'

				if event.type == pygame.QUIT:
					pygame.quit()
					return ('rage-quit', None, None, None, None)

		while not select_bridge:
			self.clock.tick(30)
			for event in pygame.event.get():
				if event.type == pygame.MOUSEBUTTONUP:
					pos = pygame.mouse.get_pos()
					x = int(pos[0]/50)
					y = int(pos[1]/50)
					if x < state.size*2 - 1 and y < state.size*2 - 1:
						if x % 2 == 1 and y % 2 == 0:
							x = int((x-1)/2)
							y = int(y/2)
							if state.h_bridges[y][x]:
								select_bridge = True
								action = (pawn_id,dir,'h',x,y)
						elif x % 2 == 0 and y % 2 == 1:
							x = int(x / 2)
							y = int((y  - 1) / 2)
							if state.v_bridges[y][x]:
								select_bridge = True
								action = (pawn_id, dir, 'v', x, y)

				if event.type == pygame.QUIT:
					pygame.quit()
					return ('rage-quit', None, None, None, None)
		return action
  
	def get_name(self):
		return "human agent"