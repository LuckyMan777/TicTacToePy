import random
from utils import get_1d_index, get_2d_indices, get_other_player
from tqdm import tqdm

'''
Board:
0 1 2
3 4 5 
6 7 8
'''


class State(object):

    def __init__(self, board=None, next_player=1, ai_num=1):
        if board is None:
            board = [0 for _ in range(9)]
        self.board = board
        self.next_player = next_player
        self.ai_num = ai_num
        self._moves_corners = [0, 2, 6, 8]
        self._moves_others = [1, 3, 5, 7]
        random.shuffle(self._moves_corners)
        random.shuffle(self._moves_others)

    def _best_moves(self) -> list:
        """
        :return: The first element is central position, then the corners follow and then the rest
        """
        return [4] + self._moves_corners + self._moves_others

    def check_win(self, num_player: int) -> (bool, int, int, int):
        """
        :param num_player: Player number to check win
        :return: The win of the player and positions of the winning cells
        """
        for i in range(3):
            # check horizontal lines
            if self.board[get_1d_index(i, 0)] == self.board[get_1d_index(i, 1)] == \
                    self.board[get_1d_index(i, 2)] == num_player:
                return True, get_1d_index(i, 0), get_1d_index(i, 1), get_1d_index(i, 2)

            # check vertical lines
            if self.board[get_1d_index(0, i)] == self.board[get_1d_index(1, i)] == \
                    self.board[get_1d_index(2, i)] == num_player:
                return True, get_1d_index(0, i), get_1d_index(1, i), get_1d_index(2, i)

        # check diagonal lines
        if self.board[get_1d_index(0, 0)] == self.board[get_1d_index(1, 1)] == \
                self.board[get_1d_index(2, 2)] == num_player:
            return True, get_1d_index(0, 0), get_1d_index(1, 1), get_1d_index(2, 2)

        if self.board[get_1d_index(2, 0)] == self.board[get_1d_index(1, 1)] == \
                self.board[get_1d_index(0, 2)] == num_player:
            return True, get_1d_index(2, 0), get_1d_index(1, 1), get_1d_index(0, 2)

        return False, None, None, None

    def check_draw(self) -> bool:
        if self.check_win(1)[0] or self.check_win(2)[0]:
            return False
        if self.board.count(0) > 0:
            return False
        return True

    def check_terminal_state(self) -> bool:
        return self.check_win(1)[0] or self.check_win(2)[0] or self.check_draw()

    def get_empty_indices(self) -> list:
        return [ind for ind, x in enumerate(self.board) if x == 0]

    def make_move(self, cell: (int, int), num_player=None):
        """
        :param cell: The cell to place player's label
        :param num_player: Player who needs to make a move
        :return: The new state if move is allowed, otherwise old state.
        """
        if num_player is None:
            num_player = self.next_player

        index_1d = get_1d_index(cell[0], cell[1])
        if self.board[index_1d] == 0:
            new_board = self.board.copy()
            new_board[index_1d] = num_player
            return State(new_board, get_other_player(num_player), ai_num=self.ai_num)
        else:
            return self

    def _get_childrens(self):
        childrens = []
        for ind in self.get_empty_indices():
            indices_2d = get_2d_indices(ind)
            childrens.append(self.make_move(indices_2d))
        # random.shuffle(childrens)
        return zip(childrens, self.get_empty_indices())

    def _get_manhattan_distance_to_cell(self, cell: (int, int)) -> int:
        """
        :return: Summary manhattan distance from cell to every opponent's cell
        """
        opponent_cells = [ind for ind, val in enumerate(self.board) if val == get_other_player(self.next_player)]

        if len(opponent_cells) == 0:
            return 0

        manh_sum = 0
        for ind in opponent_cells:
            indices_2d = get_2d_indices(ind)
            manh_sum += abs(indices_2d[0] - cell[0]) + abs(indices_2d[1] - cell[1])
        return manh_sum

    def _simple_alg(self):
        """
        Simple algorithm, based on If's
        :return: new State and Move to get new State
        """
        # If can win -> do it
        for children, move in self._get_childrens():
            if children.check_win(self.next_player)[0]:
                return children, get_2d_indices(move)

        # If can lose -> block it
        possible_moves = self.get_empty_indices()
        for ind in possible_moves:
            opp_state = self.make_move(get_2d_indices(ind), get_other_player(self.next_player))
            if opp_state.check_win(get_other_player(self.next_player))[0]:
                block_state = self.make_move(get_2d_indices(ind))
                return block_state, get_2d_indices(ind)

        # Check tricky opponent's combination (opposite corners used)
        cnt_xs = len([val for val in self.board if val == 1])
        if cnt_xs == 2 and self.ai_num == 2 and (
                self.board[0] == self.board[8] == 1 or self.board[2] == self.board[6] == 1):
            move = get_2d_indices(random.choice(self._moves_others))
            return self.make_move(move), move

        # Sort corner cells by decreasing distance to opponent's cells if ai_num == 1.
        # Else sort by increasing distance.
        reverse = True if self.ai_num == 1 else False
        self._moves_corners = list(sorted(self._moves_corners,
                                          key=lambda index: self._get_manhattan_distance_to_cell(get_2d_indices(index)),
                                          reverse=reverse))
        # Choosing best possible move
        resorted_moves = [move for move in self._best_moves() if move in possible_moves]
        if len(resorted_moves) == 0:
            return self, None
        return self.make_move(get_2d_indices(resorted_moves[0])), get_2d_indices(resorted_moves[0])

    def get_next_move(self) -> (int, int):
        """
        :return: Best possible move
        """
        # return self._minimax_alg()[1]
        return self._simple_alg()[1]

    def get_random_move(self) -> (int, int):
        """
        :return: Random move
        """
        possible_moves = self.get_empty_indices()
        return get_2d_indices(random.choice(possible_moves)) if len(possible_moves) > 0 else (None, None)

    def _get_heuristic(self) -> int:
        if not self.check_terminal_state():
            return 0
        if self.check_win(get_other_player(self.next_player)):
            return 30
        if self.check_win(self.next_player):
            return -30
        return 15

    def _minimax_alg(self, depth: int = 9):
        if depth == 0 or self.check_terminal_state():
            return self._get_heuristic(), (None, None)  # - (10 - depth), (None, None)
        best_score = 100
        best_move = (None, None)
        for children, ind in self._get_childrens():
            if depth == 9:
                print(ind, end=' ')
                print()
            children_score, _ = children._minimax_alg(depth - 1)
            children_score *= -1
            if children_score < best_score:
                best_score = children_score
                best_move = get_2d_indices(ind)
        return best_score, best_move

    def print_board(self):
        for row_num in range(3):
            for col_num in range(3):
                print(self.board[get_1d_index(row_num, col_num)], end=' ')
            print()
        print()


def test_ai(ai_num: int) -> bool:
    states = []
    state = State(ai_num=ai_num)
    random_move = False if ai_num == 1 else True

    while not state.check_terminal_state():
        if random_move:
            state = state.make_move(state.get_random_move())
            states.append(state)
        else:
            state = state.make_move(state.get_next_move())
            states.append(state)
        random_move = not random_move

    condition = state.check_win(state.ai_num)
    condition = condition or state.check_draw() if ai_num == 2 else condition

    if not condition:
        for state in states:
            state.print_board()

    return condition


if __name__ == "__main__":
    s = State(next_player=1)
    # s = s.make_move((0, 0)).make_move((0, 1))
    s.print_board()

    while not s.check_terminal_state():
        s = s.make_move(s.get_next_move())
        s.print_board()

    print("Check draw: {}".format(s.check_draw()))
    '''
    for _ in tqdm(range(10000)):
       if not test_ai(2):
            break
    '''