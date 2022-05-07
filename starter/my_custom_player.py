from copy import deepcopy
import math
import random
import sys
from isolation import Isolation, DebugState
from sample_players import DataPlayer

from operator import itemgetter

import timeit

SEED = None


class CustomPlayer(DataPlayer):
    """Implement your own agent to play knight's Isolation

    The get_action() method is the only required method for this project.
    You can modify the interface for get_action by adding named parameters
    with default values, but the function MUST remain compatible with the
    default interface.

    **********************************************************************
    NOTES:
    - The test cases will NOT be run on a machine with GPU access, nor be
      suitable for using any other machine learning techniques.

    - You can pass state forward to your agent on the next turn by assigning
      any pickleable object to the self.context attribute.
    **********************************************************************
    """

    def __init__(self, player_id, seed=SEED):
        self.player = player_id
        self.random = random.Random(seed)

    def get_action(self, state: Isolation) -> None:
        """Employ an adversarial search technique to choose an action
        available in the current state calls self.queue.put(ACTION) at least

        This method must call self.queue.put(ACTION) at least once, and may
        call it as many times as you want; the caller will be responsible
        for cutting off the function after the search time limit has expired.

        See RandomPlayer and GreedyPlayer in sample_players for more examples.

        **********************************************************************
        NOTE:
        - The caller is responsible for cutting off search, so calling
          get_action() from your own code will create an infinite loop!
          Refer to (and use!) the Isolation.play() function to run games.
        **********************************************************************
        """
        self.queue.put(
            random.choice(state.actions())
        )  # fallback to make sure we do not get stuck
        next_move = None
        if state.ply_count < 2:
            next_move = self.get_opening_move(state)
        else:
            start = timeit.default_timer()
            next_move = self.get_next_move(state, max_depth=5)
            end = timeit.default_timer()
            took_ms = (end - start) * 1000
            if took_ms > 450:
                print("Search took {}ms".format(took_ms, 2))
        self.queue.put(next_move)

    def get_opening_move(self, state: Isolation):
        return random.choice(state.actions())

    def get_next_move(self, state: Isolation, max_depth: int):
        # If there is only one valid move, return that move
        allowed_moves = state.actions()
        if len(allowed_moves) == 1:
            return allowed_moves[0]

        moves_and_scores = []
        for move in allowed_moves:
            minimax_score = self.minimax(
                self.player, max_depth, state, move, -sys.maxsize, sys.maxsize
            )
            moves_and_scores.append([move, minimax_score])

        scores = [item[1] for item in moves_and_scores]
        max_score = max(scores)

        potential_moves = []
        for move_and_score in moves_and_scores:
            if move_and_score[1] == max_score:
                potential_moves.append(move_and_score[0])

        return self.random.choice(potential_moves)

    def minimax(self, player, depth, state: Isolation, move, alpha, beta):
        if state.terminal_test():
            return state.utility(self.player)
        if depth == 0:
            return self.liberties_heuristics_keep_enemy_close(state)

        test_board = state.result(move)

        maxi = test_board.player() == player

        move_options = test_board.actions()
        # TODO: How to sort moves to help alpha-beta pruning and how to evaluate its effectiveness?
        # This seems to be slower...
        # move_options_with_scores = [(move, self.liberties_heuristics(test_board.result(move)) ) for move in move_options]
        # move_options_with_scores = sorted(move_options_with_scores, key=itemgetter(1), reverse=True if maxi else False)
        # move_options = [x[0] for x in move_options_with_scores]
    
        best_move = -sys.maxsize if maxi else sys.maxsize

        for move_slot in move_options:
            current_value = self.minimax(
                player, depth - 1, test_board, move_slot, alpha, beta
            )

            if maxi:
                best_move = max(current_value, best_move)
                alpha = max(alpha, best_move)
            else:
                best_move = min(current_value, best_move)
                beta = min(beta, best_move)

            if beta <= alpha:
                return best_move

        return best_move

    def liberties_heuristics(self, state: Isolation):
        own_loc = state.locs[self.player]
        opp_loc = state.locs[1 - self.player]
        own_liberties = state.liberties(own_loc)
        opp_liberties = state.liberties(opp_loc)
        return len(own_liberties) - len(opp_liberties)

    def liberties_heuristics_prioritize_lower_ply_counts(self, state: Isolation):
        own_loc = state.locs[self.player]
        opp_loc = state.locs[1 - self.player]
        own_liberties = state.liberties(own_loc)
        opp_liberties = state.liberties(opp_loc)
        return len(own_liberties) - len(opp_liberties) + (state.ply_count)/2

    def liberties_heuristics_keep_enemy_close(self, state: Isolation):
        own_loc = state.locs[self.player]
        opp_loc = state.locs[1 - self.player]
        own_liberties = state.liberties(own_loc)
        opp_liberties = state.liberties(opp_loc)

        debug_state = DebugState.from_state(state)
        (own_loc_x, own_loc_y) = debug_state.ind2xy(own_loc)
        (opp_loc_x, opp_loc_y) = debug_state.ind2xy(opp_loc)

        distance = math.sqrt( (opp_loc_x - own_loc_x)**2 + (opp_loc_y - own_loc_y)**2 )

        return len(own_liberties) - len(opp_liberties) - distance/10

    def depth_liberties_heuristics(self, state: Isolation):
        own_loc = state.locs[self.player]
        opp_loc = state.locs[1 - self.player]
    
        own_liberties = state.liberties(own_loc)
        cnt_own_liberties = len(own_liberties)
        for loc in own_liberties:
            cnt_own_liberties += len(state.liberties(loc))

        opp_liberties = state.liberties(opp_loc)
        cnt_opp_liberties = len(opp_liberties)
        for loc in opp_liberties:
            cnt_opp_liberties += len(state.liberties(loc))

        return cnt_own_liberties - cnt_opp_liberties

    def liberties_heuristics_conservative(self, state: Isolation):
        own_loc = state.locs[self.player]
        opp_loc = state.locs[1 - self.player]
        own_liberties = state.liberties(own_loc)
        opp_liberties = state.liberties(opp_loc)
        return len(own_liberties)*2 - len(opp_liberties)

    def liberties_heuristics_offensive(self, state: Isolation):
        own_loc = state.locs[self.player]
        opp_loc = state.locs[1 - self.player]
        own_liberties = state.liberties(own_loc)
        opp_liberties = state.liberties(opp_loc)
        return len(own_liberties) - len(opp_liberties)*2
