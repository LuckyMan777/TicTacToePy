from tkinter import *
from functools import partial


class Board(object):
    """Graphic board"""
    _cell_size = 150

    def _init_window(self):
        self.window = Tk()
        self.window.title("Tic-Tac-Toe")
        self.window.geometry(str(Board._cell_size * 5) + 'x' + str(Board._cell_size * 3))
        # self.window.grid_rowconfigure(3, minsize=20)
        # self.window.grid_columnconfigure(5, minsize=20)

    def _init_cells(self):
        self.cells = []
        for ind in range(9):
            col_num = ind % 3
            row_num = ind // 3
            btn = Button(self.window, text=str(ind), font='arial ' + str((Board._cell_size * 2) // 3), state='disabled',
                         command=partial(self._button_cell_clicked, row_num, col_num))
            btn.place(x=Board._cell_size * col_num, y=Board._cell_size * row_num,
                      width=Board._cell_size, height=Board._cell_size)
            self.cells.append(btn)

    def __init__(self):
        self._init_window()
        self._init_cells()
        btn_first = Button(self.window, text='Играть первым', font='arial 14',
                           command=lambda: self._button_man_is_first_clicked())
        btn_first.place(x=Board._cell_size * 3 + Board._cell_size // 3, y=Board._cell_size // 3,
                        width=Board._cell_size + Board._cell_size // 3,
                        height=Board._cell_size - Board._cell_size // 3)
        self.btn_play_first = btn_first

        btn_second = Button(self.window, text='Играть вторым', font='arial 14',
                            command=lambda: self._button_man_is_second_clicked())
        btn_second.place(x=Board._cell_size * 3 + Board._cell_size // 3, y=Board._cell_size * 2,
                         width=Board._cell_size + Board._cell_size // 3,
                         height=Board._cell_size - Board._cell_size // 3)
        self.btn_play_second = btn_second

        self.board = []

    def set_cell(self, row_num: int, col_num: int, char: str):
        self.cells[row_num * 3 + col_num].configure(text=char)

    def cells_win(self, row_num1: int, col_num1: int,
                  row_num2: int, col_num2: int,
                  row_num3: int, col_num3: int):
        self.cells[row_num1 * 3 + col_num1].configure(bg="red")
        self.cells[row_num2 * 3 + col_num2].configure(bg="red")
        self.cells[row_num3 * 3 + col_num3].configure(bg="red")

    def _enable_cells(self):
        for cell in self.cells:
            cell.configure(state='normal')

    def _disable_cells(self):
        for cell in self.cells:
            cell.configure(state='disabled')

    def _button_man_is_first_clicked(self):
        self.mans_char = "X"
        self._enable_cells()

    def _button_man_is_second_clicked(self):
        self.mans_char = "O"
        self._enable_cells()

    def _button_cell_clicked(self, row_num: int, col_num: int):
        print(row_num, ' ', col_num)
        self.set_cell(row_num, col_num, self.mans_char)

    def start(self):
        # self.set_cell(1, 2, "O")
        # self.cells_win(0, 0, 1, 1, 2, 2)
        self.window.mainloop()


# window = Tk()
# window.title("Добро пожаловать в приложение PythonRu")
# window.mainloop()


b = Board()
b.start()
