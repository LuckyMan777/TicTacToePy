import random
import utils


class State(object):

    def __init__(self, board=None, next_player=1, ai_num=1):
        if board is None:
            board = [0 for _ in range(9)]
        self.board = board
        self.next_player = next_player
        self.ai_num = ai_num
        best_moves_corners = [0, 2, 6, 8]
        best_moves_others = [1, 3, 5, 7]
        random.shuffle(best_moves_corners)
        random.shuffle(best_moves_others)
        self.best_moves = [4] + best_moves_corners + best_moves_others

    def check_win(self, num_player: int):
        for i in range(3):
            # check horizontal lines
            if self.board[utils.get_1d_index(i, 0)] == self.board[utils.get_1d_index(i, 1)] == \
                    self.board[utils.get_1d_index(i, 2)] == num_player:
                return True, utils.get_1d_index(i, 0), utils.get_1d_index(i, 1), utils.get_1d_index(i, 2)
            # check vertical lines
            if self.board[utils.get_1d_index(0, i)] == self.board[utils.get_1d_index(1, i)] == \
                    self.board[utils.get_1d_index(2, i)] == num_player:
                return True, utils.get_1d_index(0, i), utils.get_1d_index(1, i), utils.get_1d_index(2, i)

        # check diagonal lines
        if self.board[utils.get_1d_index(0, 0)] == self.board[utils.get_1d_index(1, 1)] == \
                self.board[utils.get_1d_index(2, 2)] == num_player:
            return True, utils.get_1d_index(0, 0), utils.get_1d_index(1, 1), utils.get_1d_index(2, 2)
        if self.board[utils.get_1d_index(2, 0)] == self.board[utils.get_1d_index(1, 1)] == \
                self.board[utils.get_1d_index(0, 2)] == num_player:
            return True, utils.get_1d_index(2, 0), utils.get_1d_index(1, 1), utils.get_1d_index(0, 2)

        return False

    def check_draw(self):
        if self.check_win(1)[0] or self.check_win(2)[0]:
            return False
        if self.board.count(0) > 0:
            return False
        return True

    def get_heuristic(self):
        if self.check_win(get_other_player(self.next_player))[0]:
            return 10  # - len(self.get_empty_indices())
        if self.check_win(self.next_player)[0]:
            return -10  # + len(self.get_empty_indices())
        if self.check_draw():
            return 2
        return 0

    def is_terminal_state(self):
        return self.check_win(1)[0] or self.check_win(2)[0] or self.check_draw()

    def get_empty_indices(self):
        return [ind for ind, x in enumerate(self.board) if x == 0]

    def make_move(self, cell: (int, int), num_player=None):
        if num_player is None:
            num_player = self.next_player
        index_1d = utils.get_1d_index(cell[0], cell[1])
        if self.board[index_1d] == 0:
            new_board = self.board.copy()
            new_board[index_1d] = num_player
            return State(new_board, get_other_player(num_player))
        else:
            return self

    def get_childrens(self):
        childrens = []
        for ind in self.get_empty_indices():
            childrens.append(self.make_move(utils.get_2d_indices(ind)))
        # random.shuffle(childrens)
        return zip(childrens, self.get_empty_indices())

    def minimax(self, maximizing=True, depth=0):
        if self.is_terminal_state():
            if self.check_win(1)[0]:
                return 10 - depth, None
            elif self.check_win(2)[0]:
                return -10 + depth, None
            elif self.check_draw():
                return 0, None

        best = 10
        best = -best if maximizing else best
        for children_state, move in self.get_childrens():
            children_score, _ = children_state.minimax(not maximizing, depth + 1)
            if maximizing:
                if children_score > best:
                    best, best_move = children_score, move
            else:
                if children_score < best:
                    best, best_move = children_score, move

        return best, best_move

    def alphabeta(self, depth, a=-100, b=100, maximizing=True):
        if depth == 0 or self.is_terminal_state():
            return self.get_heuristic(), None
        best = -100 if maximizing else 100
        for children_state, move in self.get_childrens():
            if maximizing:
                best = max(best, children_state.alphabeta(depth - 1, a, b, False)[0])
                a = max(a, best)
            else:
                best = min(best, children_state.alphabeta(depth - 1, a, b, True)[0])
                b = min(b, best)
            if a >= b:
                break
        return best, move

    def simple_alg(self):
        for children, move in self.get_childrens():
            if children.check_win(self.next_player)[0]:
                return children, move
        possible_moves = self.get_empty_indices()
        for ind in possible_moves:
            opp_state = self.make_move(utils.get_2d_indices(ind), get_other_player(self.next_player))
            if opp_state.check_win(get_other_player(self.next_player))[0]:
                block_state = self.make_move(utils.get_2d_indices(ind))
                return block_state, ind
        resorted_moves = [move for move in self.best_moves if move in possible_moves]
        if len(resorted_moves) == 0:
            return self, None
        return self.make_move(utils.get_2d_indices(resorted_moves[0])), resorted_moves[0]

    def get_next_move(self):
        # score, move = state.alphabeta(3)
        # print('score = {}, move = {}'.format(score, move))
        # return state.make_move(utils.get_2d_indices(move))

        # for i in range(1, 10):
        #    iscore, istate, idepth, imove = max_score(state, i)
        #    print('max_depth = {}, best_depth = {}, score = {} move = {}'.format(i, idepth, iscore, imove))
        # istate.print_board()
        # return max_score(state, 6)[1]
        return self.simple_alg()[1]

    def print_board(self):
        for row_num in range(3):
            for col_num in range(3):
                print(self.board[utils.get_1d_index(row_num, col_num)], end=' ')
            print()
        print()


def get_other_player(num_player: int):
    return 2 if num_player == 1 else 1


def max_score(current_state: State, depth):
    if depth == 0 or current_state.is_terminal_state():
        return current_state.get_heuristic(), current_state, depth, None
    best_score = -100
    best_depth = 0
    for children, move in current_state.get_childrens():
        children_score, _, terminal_depth, _ = min_score(children, depth - 1)
        if children_score > best_score or (children_score == best_score and terminal_depth > best_depth):
            best_score = children_score
            current_state = children
            best_depth = terminal_depth
    return best_score, current_state, best_depth, move


def min_score(current_state: State, depth):
    if depth == 0 or current_state.is_terminal_state():
        return -current_state.get_heuristic(), current_state, depth, None
    best_score = 100
    best_depth = 0
    best_move = None
    for children, move in current_state.get_childrens():
        children_score, _, terminal_depth, _ = max_score(children, depth - 1)
        if children_score < best_score or (children_score == best_score and terminal_depth > best_depth):
            best_score = children_score
            current_state = children
            best_depth = terminal_depth
            best_move = move
    return best_score, current_state, best_depth, best_move


def get_next_step(state: State):
    # score, move = state.alphabeta(3)
    # print('score = {}, move = {}'.format(score, move))
    # return state.make_move(utils.get_2d_indices(move))

    # for i in range(1, 10):
    #    iscore, istate, idepth, imove = max_score(state, i)
    #    print('max_depth = {}, best_depth = {}, score = {} move = {}'.format(i, idepth, iscore, imove))
    # istate.print_board()
    # return max_score(state, 6)[1]
    return state.simple_alg()[0]



if __name__ == "__main__":
    s = State(next_player=1)
    # s = s.get_childrens()[0].get_childrens()[1].get_childrens()[0].get_childrens()[1].get_childrens()[-1].get_childrens()[-1]#.get_childrens()[-1]
    # s = s.get_childrens()[4].get_childrens()[1].get_childrens()[0]#.get_childrens()[-1].get_childrens()[-2]
    s = s.make_move((1, 1)).make_move((0, 1)).make_move((2, 2)).make_move((0, 0)).make_move((0, 2)).make_move((2, 0))
    s.print_board()

    while (not s.is_terminal_state()):
        s = get_next_step(s)
        s.print_board()

    s.print_board()
    print(s.check_draw())

    # score1, state1 = max_score(s, 9)
    # state1.print_board()
