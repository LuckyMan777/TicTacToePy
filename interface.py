from tkinter import *
from functools import partial
from utils import get_1d_index, get_2d_indices, get_other_player
from state import State


class Interface(object):
    """Interface of tic tac toe"""
    _cell_size = 150
    _text_color = 'black'
    _cell_color_normal = 'gray90'
    _cell_color_ai_win = 'red1'
    _cell_color_human_win = 'green2'
    _cell_color_draw = 'yellow1'
    _button_text_font = 'arial 18'

    def _init_window(self):
        self.window = Tk()
        self.window.title('Tic-Tac-Toe')
        self.window.geometry(str(Interface._cell_size * 5) + 'x' + str(Interface._cell_size * 3))

    def _init_cells(self):
        """
        Size of chars in cells is (Interface._cell_size * 2) // 3
        """
        self.cells = []
        for ind in range(9):
            row_num, col_num = get_2d_indices(ind)
            btn = Button(self.window, text='', font='arial ' + str((Interface._cell_size * 2) // 3),
                         bg=Interface._cell_color_normal, fg=Interface._text_color,
                         command=partial(self._button_cell_clicked, (row_num, col_num)))
            btn.place(x=Interface._cell_size * col_num, y=Interface._cell_size * row_num,
                      width=Interface._cell_size, height=Interface._cell_size)
            self.cells.append(btn)

    def _init_buttons(self):
        """
        First button:
            placed (Interface._cell_size // 3) pixels to the right of the cells
                and (Interface._cell_size // 3) pixels below the top border
        Second button:
            placed (Interface._cell_size // 3) pixels to the right of the cells
                and (Interface._cell_size // 3) pixels above the lower border
        Size of buttons is (Interface._cell_size * 4 // 3, Interface._cell_size * 2 // 3)
        """
        btn_first = Button(self.window, text='Играть первым', font=Interface._button_text_font,
                           command=lambda: self._button_human_clicked(1))
        btn_first.place(x=Interface._cell_size * 3 + Interface._cell_size // 3, y=Interface._cell_size // 3,
                        width=(Interface._cell_size * 4) // 3,
                        height=(Interface._cell_size * 2) // 3)
        self.btn_play_first = btn_first

        btn_second = Button(self.window, text='Играть вторым', font=Interface._button_text_font,
                            command=lambda: self._button_human_clicked(2))
        btn_second.place(x=Interface._cell_size * 3 + Interface._cell_size // 3, y=Interface._cell_size * 2,
                         width=(Interface._cell_size * 4) // 3,
                         height=(Interface._cell_size * 2) // 3)
        self.btn_play_second = btn_second

    def __init__(self):
        self._init_window()
        self._init_cells()
        self._init_buttons()
        self.end_game = True

    def _clear_cells(self):
        """
        Update text in cells to '' and reset color of cells to normal
        """
        for cell in self.cells:
            cell.configure(text='', fg=Interface._text_color, bg=Interface._cell_color_normal)

    def _button_human_clicked(self, num: int):
        """
        Update cells and state on button click by human
        :param num: chosen number by human
        """
        humans_dict = {1: "X", 2: "O"}
        comps_dict = {1: "O", 2: "X"}
        self.humans_char = humans_dict[num]
        self.comps_char = comps_dict[num]
        self.end_game = False
        self._clear_cells()
        self.state = State(ai_num=2)
        if num == 2:
            self.state.ai_num = 1
            self._ai_move()

    def _button_cell_clicked(self, cell: (int, int)):
        """
        Update state and cell on cell click by human
        :param cell: cell for moving
        """
        if not self.end_game and get_1d_index(cell[0], cell[1]) in self.state.get_empty_indices():
            print(cell[0], ' ', cell[1])
            self._set_cell(cell, self.humans_char)
            self.state = self.state.make_move(cell)
            self._check_terminal_state()
            self.state.print_board()
            self._ai_move()

    def _set_cell(self, cell: (int, int), char: str):
        """
        Change text on cell to char
        """
        self.cells[get_1d_index(cell[0], cell[1])].configure(text=char, fg=Interface._text_color)

    def _set_cells_win(self, cell1: (int, int), cell2: (int, int), cell3: (int, int), color: str):
        """
        Change cells color to color variable
        """
        self.cells[get_1d_index(cell1[0], cell1[1])].configure(bg=color)
        self.cells[get_1d_index(cell2[0], cell2[1])].configure(bg=color)
        self.cells[get_1d_index(cell3[0], cell3[1])].configure(bg=color)

    def _ai_move(self):
        """
        Get best move by AI and update state and chosen cell
        """
        if not self.end_game:
            ai_move = self.state.get_next_move()
            print('ai_move = ', ai_move)
            self._set_cell(ai_move, self.comps_char)
            self.state = self.state.make_move(ai_move)
            self._check_terminal_state()
            self.state.print_board()

    def _check_terminal_state(self):
        """
        Update color of cells if terminal state
        """
        if self.state.check_terminal_state():
            is_win, cell1, cell2, cell3 = self.state.check_win(self.state.ai_num)
            if is_win:
                self._set_cells_win(get_2d_indices(cell1), get_2d_indices(cell2),
                                    get_2d_indices(cell3), Interface._cell_color_ai_win)

            is_win, cell1, cell2, cell3 = self.state.check_win(get_other_player(self.state.ai_num))
            if is_win:
                self._set_cells_win(get_2d_indices(cell1), get_2d_indices(cell2),
                                    get_2d_indices(cell3), Interface._cell_color_human_win)

            if self.state.check_draw():
                for cell in self.cells:
                    cell.configure(bg=Interface._cell_color_draw)

            self.end_game = True

    def start(self):
        self.window.mainloop()
