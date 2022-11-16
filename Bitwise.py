def set_bit(value, bit):
    return value | (1 << bit)


def clear_bit(value, bit):
    return value & ~(1 << bit)


def get_pieces_num(value, col):
    return (value & (3 << col * 9)) >> col * 9


def increase_pieces_num(value, col):
    return value + (1 << col * 9)


def get_state(state, col, turn):
    pieces_num = get_pieces_num(state, col)
    if pieces_num == 7:
        return None
    bit_num = (pieces_num + 3) + 9 * col
    child_state = increase_pieces_num(state, col)
    if turn:
        return set_bit(child_state, bit_num)
    else:
        return clear_bit(child_state, bit_num)


def convert_to_matrix(state):
    matrix = [[None for i in range(7)] for j in range(6)]
    print(matrix)
    mask = 0b111111111
    for i in range(7):
        col = (state >> 9*i) & mask
        pieces_num = 3 & col
        col = col >> 3
        print(pieces_num)
        for j in range(pieces_num):
            if col & 1 == 1:
                matrix[5-j][i] = True
            else:
                matrix[5-j][i] = False
            col = col >> 1
    return matrix

statex = 0
x = statex
x = get_state(x, 0, True)
x = get_state(x, 0, False)
x = get_state(x, 0, True)
x = get_state(x, 0, True)
x = get_state(x, 0, True)

print(convert_to_matrix(x))
print(f"{x:064b}")

print(f"{x:064b}")
print(convert_to_matrix(x))
val = increase_pieces_num(statex, 2)
val = increase_pieces_num(val, 2)
val = increase_pieces_num(val, 2)
#print(get_col(val, 2))
#print(f"{increase_col(val, 1):064b}")
