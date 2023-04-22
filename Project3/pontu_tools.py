from pontu_gui import *
from pontu_state import PontuState
import time
import signal
import traceback
from threading import Thread

def play_game(init_state, names, players, total_time, display_gui):
    # create the initial state
    state = init_state
    # initialize the time left for each player
    time_left = [total_time for _ in range(len(players))]
    timedout = -1
    crashed = -1
    invalidaction = -1
    quit = -1
    exception = ''
    action = None
    last_action = None
    if display_gui:
        gui = GUIState()
    # loop until the game is over

    while not state.game_over():
        cur_player = state.get_cur_player()
        timer_stop = [False]
        if display_gui:
            timer = TimerDisplay(gui, cur_player, time_left.copy(), timer_stop)
            gui.display_state(state)
            pygame.display.flip()
            timer.start()
        try:
            action, exe_time = get_action_timed(players[cur_player], state, last_action, time_left[cur_player])
        except TimeoutError:
            # set that the current player timed out
            timedout = cur_player
            state.set_timed_out(cur_player)
            break
        except Exception as e:
            trace = traceback.format_exc().split('\n')
            exception = trace[len(trace) - 2]
            # set that the current player crashed
            crashed = cur_player
            raise e
            break
        else:
            # update time
            timer_stop[0] = True
            time_left[cur_player] -= exe_time
            # check if the action is valid
            try:
                if action[0] == 'rage-quit':
                    # the player wants to quit
                    quit = cur_player
                    state.winner = 1 - quit
                    break
                elif state.is_action_valid(action):
                    # the action is valid so we can apply the action to the state
                    state.apply_action(action)
                    last_action = action
                else:
                    print('invalid ' + str(action))
                    # set that the current player gave an invalid action
                    invalidaction = cur_player
                    state.set_invalid_action(invalidaction)
                    break
            except Exception:
                # set that the current player gave an invalid action
                invalidaction = cur_player
                state.set_invalid_action(cur_player)
                break
        if display_gui:
            timer.join()
    if display_gui:
        gui.display_winner(state)

    # output the result of the game: 0 if player 0 wins, 1 if player 1 wins and -1 if it is a draw
    # first check if there was timeout, crash, invalid action or quit
    if timedout != -1:
        return (1 - timedout, names[timedout] + ' timed out', total_time - time_left[0], total_time - time_left[1],
                state.get_scores())
    elif crashed != -1:
        return (
        1 - crashed, names[crashed] + ' crashed: ' + exception, total_time - time_left[0], total_time - time_left[1],
        state.get_scores())
    elif invalidaction != -1:
        return (
        1 - invalidaction, names[invalidaction] + ' gave an invalid action: ' + str(action), total_time - time_left[0],
        total_time - time_left[1], state.get_scores())
    elif quit != -1:
        return (
        1 - quit, names[quit] + ' rage quit', total_time - time_left[0], total_time - time_left[1], state.get_scores())
    else:
        # all is ok, output the winner
        return (
        state.get_winner(), 'scores: ' + str(state.get_scores()), total_time - time_left[0], total_time - time_left[1],
        state.get_scores())


"""
Get an action from player with a timeout.
"""
def get_action_timed(player, state, last_action, time_left):
	#signal.signal(signal.SIGALRM, handle_timeout)
	#signal.setitimer(signal.ITIMER_REAL, time_left)
	exe_time = time.time()
	try:
		action = player.get_action(state, last_action, time_left)
	finally:
		#signal.setitimer(signal.ITIMER_REAL, 0)
		exe_time = time.time() - exe_time
	return action, exe_time


"""
Define behavior in case of timeout.
"""
def handle_timeout(signum, frame):
    raise TimeoutError()

def handler(signum, frame):
    raise Exception('end of time')


class TimerDisplay(Thread):

    def __init__(self, board, cur_player, times_left, stopped):
        Thread.__init__(self)
        self.board = board
        self.cur_player = cur_player
        self.times_left = times_left
        self.stopped = stopped

    def run(self):
        beg_time = time.time()
        delta = self.times_left[self.cur_player] % 1
        self.board.show_timer(self.times_left)
        pygame.display.flip()

        clock = pygame.time.Clock()
        while not self.stopped[0] and self.times_left[self.cur_player] > 0:
            clock.tick(30)
            if time.time() - beg_time >= delta:
                self.times_left[self.cur_player] -= 1
                self.board.show_timer(self.times_left)
                pygame.display.flip()
                delta += 1