from tkinter import *
from functools import partial
import utils
import tic_tac_toe


class Interface(object):
    """Interface of tic tac toe"""
    _cell_size = 150

    def _init_window(self):
        self.window = Tk()
        self.window.title("Tic-Tac-Toe")
        self.window.geometry(str(Interface._cell_size * 5) + 'x' + str(Interface._cell_size * 3))

    def _init_cells(self):
        self.cells = []
        for ind in range(9):
            row_num, col_num = utils.get_2d_indices(ind)
            btn = Button(self.window, text="", font='arial ' + str((Interface._cell_size * 2) // 3), bg="gray",
                         state='disabled', command=partial(self._button_cell_clicked, (row_num, col_num)))
            btn.place(x=Interface._cell_size * col_num, y=Interface._cell_size * row_num,
                      width=Interface._cell_size, height=Interface._cell_size)
            self.cells.append(btn)

    def _init_buttons(self):
        btn_first = Button(self.window, text='Играть первым', font='arial 14',
                           command=lambda: self._button_man_clicked(1))
        btn_first.place(x=Interface._cell_size * 3 + Interface._cell_size // 3, y=Interface._cell_size // 3,
                        width=Interface._cell_size + Interface._cell_size // 3,
                        height=Interface._cell_size - Interface._cell_size // 3)
        self.btn_play_first = btn_first

        btn_second = Button(self.window, text='Играть вторым', font='arial 14',
                            command=lambda: self._button_man_clicked(2))
        btn_second.place(x=Interface._cell_size * 3 + Interface._cell_size // 3, y=Interface._cell_size * 2,
                         width=Interface._cell_size + Interface._cell_size // 3,
                         height=Interface._cell_size - Interface._cell_size // 3)
        self.btn_play_second = btn_second

    def __init__(self):
        self._init_window()
        self._init_cells()
        self._init_buttons()

    def clear_cells(self):
        for cell in self.cells:
            cell.configure(text="", bg="gray")

    def _enable_cells(self):
        for cell in self.cells:
            cell.configure(state='normal')

    def _disable_cells(self):
        for cell in self.cells:
            cell.configure(state='disabled')

    def _button_man_clicked(self, num: int):
        mans_dict = {1: "X", 2: "O"}
        comps_dict = {1: "O", 2: "X"}
        self.mans_char = mans_dict[num]
        self.comps_char = comps_dict[num]
        self._enable_cells()
        self.state = tic_tac_toe.State()
        if num == 2:
            self.ai_move()

    def _button_cell_clicked(self, cell: (int, int)):
        print(cell[0], ' ', cell[1])
        self.set_cell(cell, self.mans_char)
        self.state = self.state.make_move(cell)
        self.state.print_board()
        self.ai_move()

    def set_cell(self, cell: (int, int), char: str):
        self.cells[utils.get_1d_index(cell[0], cell[1])].configure(text=char)

    def set_cells_win(self, cell1: (int, int), cell2: (int, int), cell3: (int, int)):
        self.cells[utils.get_1d_index(cell1[0], cell1[1])].configure(bg="red")
        self.cells[utils.get_1d_index(cell2[0], cell2[1])].configure(bg="red")
        self.cells[utils.get_1d_index(cell3[0], cell3[1])].configure(bg="red")

    def start(self):
        # self.set_cell(1, 2, "O")
        # self.cells_win(0, 0, 1, 1, 2, 2)
        self.window.mainloop()

    def ai_move(self):
        ai_move = self.state.get_next_move()
        indices_2d = utils.get_2d_indices(ai_move)
        self.state = self.state.make_move(indices_2d)
        self.set_cell(indices_2d, self.comps_char)
        self.state.print_board()

    def check_terminal(self):
        if self.state.is_terminal_state():
            is_win, cell1, cell2, cell3 = self.state.check_win(1)
            if is_win:
                self.set_cells_win(utils.get_2d_indices(cell1), utils.get_2d_indices(cell2),
                                   utils.get_2d_indices(cell3))


b = Interface()
b.start()
