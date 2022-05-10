import random
import sys
import math
import timeit

from isolation import Isolation, DebugState
from sample_players import DataPlayer


def heuristics_liberties(state: Isolation, player: int):
    """# player_moves - # opp_moves"""
    own_loc = state.locs[player]
    opp_loc = state.locs[1 - player]
    own_liberties = state.liberties(own_loc)
    opp_liberties = state.liberties(opp_loc)
    return len(own_liberties) - len(opp_liberties)


def heuristics_liberties_player_only(state: Isolation, player: int):
    """Only # player moves"""
    own_loc = state.locs[player]
    own_liberties = state.liberties(own_loc)
    return len(own_liberties)


def heuristics_liberties_opponent_only(state: Isolation, player: int):
    """Only # opponent moves"""
    opp_loc = state.locs[1 - player]
    opp_liberties = state.liberties(opp_loc)
    return -len(opp_liberties)


def heuristics_prioritize_higher_ply_counts(state: Isolation, player: int):
    """Prioritize higher play counts (longer games)"""
    return state.ply_count


def heuristics_prioritize_lower_ply_counts(state: Isolation, player: int):
    """Prioritize lower play counts (shorter games)"""
    return -state.ply_count


# def heuristics_liberties_and_prioritize_higher_ply_counts(
#     state: Isolation, player: int
# ):
#     """Use the baseline # player_moves - # opp_moves but prioritize higher play counts (shorter games)"""
#     own_m_opp_moves = heuristics_liberties(state, player)
#     return own_m_opp_moves + state.ply_count / 2


# def heuristics_liberties_and_prioritize_lower_ply_counts(state: Isolation, player: int):
#     """Use the baseline # player_moves - # opp_moves but prioritize lower play counts (shorter games)"""
#     own_m_opp_moves = heuristics_liberties(state, player)
#     return own_m_opp_moves - state.ply_count / 2


def heuristics_keep_enemy_close(state: Isolation, player: int):
    own_loc = state.locs[player]
    opp_loc = state.locs[1 - player]

    debug_state = DebugState.from_state(state)
    (own_loc_x, own_loc_y) = debug_state.ind2xy(own_loc)
    (opp_loc_x, opp_loc_y) = debug_state.ind2xy(opp_loc)

    distance = (opp_loc_x - own_loc_x) ** 2 + (opp_loc_y - own_loc_y) ** 2

    return -distance


def heuristics_keep_enemy_far(state: Isolation, player: int):
    own_loc = state.locs[player]
    opp_loc = state.locs[1 - player]

    debug_state = DebugState.from_state(state)
    (own_loc_x, own_loc_y) = debug_state.ind2xy(own_loc)
    (opp_loc_x, opp_loc_y) = debug_state.ind2xy(opp_loc)

    distance = (opp_loc_x - own_loc_x) ** 2 + (opp_loc_y - own_loc_y) ** 2

    return distance


def heuristics_liberties_and_keep_enemy_close_1(state: Isolation, player: int):
    """Baseline # player_moves - # opp_moves while keeping the enemy close"""
    own_loc = state.locs[player]
    opp_loc = state.locs[1 - player]
    own_liberties = state.liberties(own_loc)
    opp_liberties = state.liberties(opp_loc)

    debug_state = DebugState.from_state(state)
    (own_loc_x, own_loc_y) = debug_state.ind2xy(own_loc)
    (opp_loc_x, opp_loc_y) = debug_state.ind2xy(opp_loc)

    distance = math.sqrt((opp_loc_x - own_loc_x) ** 2 + (opp_loc_y - own_loc_y) ** 2)

    return len(own_liberties) - len(opp_liberties) - distance


def heuristics_liberties_and_keep_enemy_close_2(state: Isolation, player: int):
    """Baseline # player_moves - # opp_moves while keeping the enemy close"""
    own_loc = state.locs[player]
    opp_loc = state.locs[1 - player]
    own_liberties = state.liberties(own_loc)
    opp_liberties = state.liberties(opp_loc)

    debug_state = DebugState.from_state(state)
    (own_loc_x, own_loc_y) = debug_state.ind2xy(own_loc)
    (opp_loc_x, opp_loc_y) = debug_state.ind2xy(opp_loc)

    distance = math.sqrt((opp_loc_x - own_loc_x) ** 2 + (opp_loc_y - own_loc_y) ** 2)

    return len(own_liberties) - len(opp_liberties) - distance / 2


def heuristics_liberties_and_keep_enemy_close_3(state: Isolation, player: int):
    """Baseline # player_moves - # opp_moves while keeping the enemy close"""
    own_loc = state.locs[player]
    opp_loc = state.locs[1 - player]
    own_liberties = state.liberties(own_loc)
    opp_liberties = state.liberties(opp_loc)

    debug_state = DebugState.from_state(state)
    (own_loc_x, own_loc_y) = debug_state.ind2xy(own_loc)
    (opp_loc_x, opp_loc_y) = debug_state.ind2xy(opp_loc)

    distance = math.sqrt((opp_loc_x - own_loc_x) ** 2 + (opp_loc_y - own_loc_y) ** 2)

    return len(own_liberties) - len(opp_liberties) - 2 * distance


def heuristics_liberties_and_keep_enemy_close_4(state: Isolation, player: int):
    """Baseline # player_moves - # opp_moves while keeping the enemy close"""
    own_loc = state.locs[player]
    opp_loc = state.locs[1 - player]
    own_liberties = state.liberties(own_loc)
    opp_liberties = state.liberties(opp_loc)

    debug_state = DebugState.from_state(state)
    (own_loc_x, own_loc_y) = debug_state.ind2xy(own_loc)
    (opp_loc_x, opp_loc_y) = debug_state.ind2xy(opp_loc)

    distance = math.sqrt((opp_loc_x - own_loc_x) ** 2 + (opp_loc_y - own_loc_y) ** 2)

    return len(own_liberties) - len(opp_liberties) - distance / 4


def heuristics_liberties_and_keep_enemy_close_5(state: Isolation, player: int):
    """Baseline # player_moves - # opp_moves while keeping the enemy close"""
    own_loc = state.locs[player]
    opp_loc = state.locs[1 - player]
    own_liberties = state.liberties(own_loc)
    opp_liberties = state.liberties(opp_loc)

    debug_state = DebugState.from_state(state)
    (own_loc_x, own_loc_y) = debug_state.ind2xy(own_loc)
    (opp_loc_x, opp_loc_y) = debug_state.ind2xy(opp_loc)

    distance = math.sqrt((opp_loc_x - own_loc_x) ** 2 + (opp_loc_y - own_loc_y) ** 2)

    return len(own_liberties) - len(opp_liberties) - 4 * distance


def heuristics_liberties_and_keep_enemy_close_6(state: Isolation, player: int):
    """Baseline # player_moves - # opp_moves while keeping the enemy close"""
    own_loc = state.locs[player]
    opp_loc = state.locs[1 - player]
    own_liberties = state.liberties(own_loc)
    opp_liberties = state.liberties(opp_loc)

    debug_state = DebugState.from_state(state)
    (own_loc_x, own_loc_y) = debug_state.ind2xy(own_loc)
    (opp_loc_x, opp_loc_y) = debug_state.ind2xy(opp_loc)

    distance = math.sqrt((opp_loc_x - own_loc_x) ** 2 + (opp_loc_y - own_loc_y) ** 2)

    return len(own_liberties) - len(opp_liberties) - distance / 8


def heuristics_liberties_and_keep_enemy_close_7(state: Isolation, player: int):
    """Baseline # player_moves - # opp_moves while keeping the enemy close"""
    own_loc = state.locs[player]
    opp_loc = state.locs[1 - player]
    own_liberties = state.liberties(own_loc)
    opp_liberties = state.liberties(opp_loc)

    debug_state = DebugState.from_state(state)
    (own_loc_x, own_loc_y) = debug_state.ind2xy(own_loc)
    (opp_loc_x, opp_loc_y) = debug_state.ind2xy(opp_loc)

    distance = math.sqrt((opp_loc_x - own_loc_x) ** 2 + (opp_loc_y - own_loc_y) ** 2)

    return len(own_liberties) - len(opp_liberties) - 8 * distance

def heuristics_liberties_and_keep_enemy_close_8(state: Isolation, player: int):
    """Baseline # player_moves - # opp_moves while keeping the enemy close"""
    own_loc = state.locs[player]
    opp_loc = state.locs[1 - player]
    own_liberties = state.liberties(own_loc)
    opp_liberties = state.liberties(opp_loc)

    debug_state = DebugState.from_state(state)
    (own_loc_x, own_loc_y) = debug_state.ind2xy(own_loc)
    (opp_loc_x, opp_loc_y) = debug_state.ind2xy(opp_loc)

    distance = math.sqrt((opp_loc_x - own_loc_x) ** 2 + (opp_loc_y - own_loc_y) ** 2)

    return len(own_liberties) - len(opp_liberties) - distance / 10

def heuristics_liberties_and_keep_enemy_close_9(state: Isolation, player: int):
    """Baseline # player_moves - # opp_moves while keeping the enemy close"""
    own_loc = state.locs[player]
    opp_loc = state.locs[1 - player]
    own_liberties = state.liberties(own_loc)
    opp_liberties = state.liberties(opp_loc)

    debug_state = DebugState.from_state(state)
    (own_loc_x, own_loc_y) = debug_state.ind2xy(own_loc)
    (opp_loc_x, opp_loc_y) = debug_state.ind2xy(opp_loc)

    distance = math.sqrt((opp_loc_x - own_loc_x) ** 2 + (opp_loc_y - own_loc_y) ** 2)

    return len(own_liberties) - len(opp_liberties) - distance / 12


def heuristics_liberties_and_keep_enemy_close_10(state: Isolation, player: int):
    """Baseline # player_moves - # opp_moves while keeping the enemy close"""
    own_loc = state.locs[player]
    opp_loc = state.locs[1 - player]
    own_liberties = state.liberties(own_loc)
    opp_liberties = state.liberties(opp_loc)

    debug_state = DebugState.from_state(state)
    (own_loc_x, own_loc_y) = debug_state.ind2xy(own_loc)
    (opp_loc_x, opp_loc_y) = debug_state.ind2xy(opp_loc)

    distance = math.sqrt((opp_loc_x - own_loc_x) ** 2 + (opp_loc_y - own_loc_y) ** 2)

    return len(own_liberties) - len(opp_liberties) - distance / 14

def heuristics_liberties_and_keep_enemy_close_11(state: Isolation, player: int):
    """Baseline # player_moves - # opp_moves while keeping the enemy close"""
    own_loc = state.locs[player]
    opp_loc = state.locs[1 - player]
    own_liberties = state.liberties(own_loc)
    opp_liberties = state.liberties(opp_loc)

    debug_state = DebugState.from_state(state)
    (own_loc_x, own_loc_y) = debug_state.ind2xy(own_loc)
    (opp_loc_x, opp_loc_y) = debug_state.ind2xy(opp_loc)

    distance = math.sqrt((opp_loc_x - own_loc_x) ** 2 + (opp_loc_y - own_loc_y) ** 2)

    return len(own_liberties) - len(opp_liberties) - distance / 16


def heuristics_liberties_and_keep_enemy_far(state: Isolation, player: int):
    """Baseline # player_moves - # opp_moves while keeping the enemy far"""
    own_loc = state.locs[player]
    opp_loc = state.locs[1 - player]
    own_liberties = state.liberties(own_loc)
    opp_liberties = state.liberties(opp_loc)

    debug_state = DebugState.from_state(state)
    (own_loc_x, own_loc_y) = debug_state.ind2xy(own_loc)
    (opp_loc_x, opp_loc_y) = debug_state.ind2xy(opp_loc)

    distance = math.sqrt((opp_loc_x - own_loc_x) ** 2 + (opp_loc_y - own_loc_y) ** 2)

    return len(own_liberties) - len(opp_liberties) + distance / 10


def heuristics_liberties_deep(state: Isolation, player: int):
    """Evaluate number of possible moves from current and next possitions"""
    own_loc = state.locs[player]
    opp_loc = state.locs[1 - player]

    own_liberties = state.liberties(own_loc)
    cnt_own_liberties = len(own_liberties)
    for loc in own_liberties:
        cnt_own_liberties += len(state.liberties(loc))

    opp_liberties = state.liberties(opp_loc)
    cnt_opp_liberties = len(opp_liberties)
    for loc in opp_liberties:
        cnt_opp_liberties += len(state.liberties(loc))

    return cnt_own_liberties - cnt_opp_liberties


def heuristics_liberties_conservative(state: Isolation, player: int):
    """Own moves are more important than enemy moves"""
    own_loc = state.locs[player]
    opp_loc = state.locs[1 - player]
    own_liberties = state.liberties(own_loc)
    opp_liberties = state.liberties(opp_loc)
    return len(own_liberties) * 2 - len(opp_liberties)


def heuristics_liberties_aggressive(state: Isolation, player: int):
    """Prefer tactsics where we starve the opponents moves"""
    own_loc = state.locs[player]
    opp_loc = state.locs[1 - player]
    own_liberties = state.liberties(own_loc)
    opp_liberties = state.liberties(opp_loc)
    return len(own_liberties) - len(opp_liberties) * 2


HEURISTICS_FUNCTIONS = {
    "heuristics_liberties": heuristics_liberties,
    "heuristics_liberties_player_only": heuristics_liberties_player_only,
    "heuristics_liberties_opponent_only": heuristics_liberties_opponent_only,
    "heuristics_prioritize_higher_ply_counts": heuristics_prioritize_higher_ply_counts,
    "heuristics_prioritize_lower_ply_counts": heuristics_prioritize_lower_ply_counts,
    "heuristics_keep_enemy_close": heuristics_keep_enemy_close,
    "heuristics_keep_enemy_far": heuristics_keep_enemy_far,
    "heuristics_liberties_and_keep_enemy_close_1": heuristics_liberties_and_keep_enemy_close_1,
    "heuristics_liberties_and_keep_enemy_close_2": heuristics_liberties_and_keep_enemy_close_2,
    "heuristics_liberties_and_keep_enemy_close_3": heuristics_liberties_and_keep_enemy_close_3,
    "heuristics_liberties_and_keep_enemy_close_4": heuristics_liberties_and_keep_enemy_close_4,
    "heuristics_liberties_and_keep_enemy_close_5": heuristics_liberties_and_keep_enemy_close_5,
    "heuristics_liberties_and_keep_enemy_close_6": heuristics_liberties_and_keep_enemy_close_6,
    "heuristics_liberties_and_keep_enemy_close_7": heuristics_liberties_and_keep_enemy_close_7,
    "heuristics_liberties_and_keep_enemy_close_8": heuristics_liberties_and_keep_enemy_close_8,
    "heuristics_liberties_and_keep_enemy_close_9": heuristics_liberties_and_keep_enemy_close_9,
    "heuristics_liberties_and_keep_enemy_close_10": heuristics_liberties_and_keep_enemy_close_10,
    "heuristics_liberties_and_keep_enemy_close_11": heuristics_liberties_and_keep_enemy_close_11,
    "heuristics_liberties_and_keep_enemy_far": heuristics_liberties_and_keep_enemy_far,
    "heuristics_liberties_deep": heuristics_liberties_deep,
    "heuristics_liberties_conservative": heuristics_liberties_conservative,
    "heuristics_liberties_aggressive": heuristics_liberties_aggressive,
}

SEED = None

HEURISTIC_FUNC = heuristics_liberties_and_keep_enemy_close_11


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
            next_move = self.get_next_move(state, max_depth=3)
            end = timeit.default_timer()
            took_ms = (end - start) * 1000
            if took_ms > 950:
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
            return state.utility(player)
        if depth == 0:
            return HEURISTIC_FUNC(state, player)

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
