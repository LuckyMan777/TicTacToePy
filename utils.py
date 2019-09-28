
def get_2d_indices(ind: int):
    return ind // 3, ind % 3


def get_1d_index(row_num: int, col_num: int):
    return row_num * 3 + col_num