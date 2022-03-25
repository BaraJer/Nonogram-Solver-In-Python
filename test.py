# in function get_intersection_row I chose to intersect and not to union , [1,0] , [0,1] ---> [-1,-1]

from copy import copy
from copy import deepcopy
from math import factorial as fac
import string

EMPTY_SLOTS = -1
BLACK_SLOTS = 1
WHITE_SLOTS = 0


def get_row_variations(row, blocks):
    """Returns all the possible variations for a row and
    a given constraints"""
    possible_variations = list()  # storage of the possible variations
    row_copy = copy(row)  # a copy of the row so we don't change the input
    empty_slots = [i for i in range(len(row)) if row[i] == EMPTY_SLOTS]  # the empty slots indexes of the given row

    if not blocks or blocks == [WHITE_SLOTS]:  # if blocks is empty
        return [[WHITE_SLOTS] * len(row)]

    if row.count(1) == sum(blocks):
        return [fill_zeros(row)]

    if row.count(1) == len(row):
        return [row]

    if row.count(-1) + row.count(1) < sum(blocks):
        return possible_variations

    get_row_variations_helper(row_copy, blocks, empty_slots, possible_variations, 0, 0)  # calling the helper

    return possible_variations  # returning the possible variations as a list


def get_row_variations_helper(row, blocks, empty_slots, possible_variations, blocks_idx, idx):
    """recursively goes on all the possible variations and append the suitable
     ones into the a list"""

    # if we got to situation the left empty slots and the filled ones are less than the whole blocks we backtrack

    if row.count(BLACK_SLOTS) > sum(blocks):
        return

    if row.count(BLACK_SLOTS) == sum(blocks):
        copy_of_row = copy(row)
        copy_of_row = fill_zeros(copy_of_row)
        if check_variations(copy_of_row, blocks):
            possible_variations.append(copy_of_row)
            return

    if idx == len(empty_slots):  # if we went on all the empty slots already / base case
        return

    row[empty_slots[idx]] = BLACK_SLOTS  # not filling a slot
    get_row_variations_helper(row, blocks, empty_slots, possible_variations, blocks_idx, idx + 1)
    row[empty_slots[idx]] = WHITE_SLOTS  # filling a slot
    get_row_variations_helper(row, blocks, empty_slots, possible_variations, blocks_idx, idx + 1)


def fill_zeros(row):
    """ filling empty slots with white slots"""
    for i in range(len(row)):
        if row[i] == EMPTY_SLOTS:
            row[i] = WHITE_SLOTS
    return row


def check_variations(row, blocks):
    """Checks that the variation suits the constraints given"""

    blocks_simulator = [1]  # a simulator list of a the wanted blocks
    ones = [i for i in range(len(row)) if row[i] == 1]  # the filled slots indexes
    blocks_index = 0  # index to go on the different blocks

    for i in range(len(ones) - 1):
        # check if the difference between filled slot index and the next slot index is 1 then they are one block
        if ones[i] + 1 == ones[i + 1]:
            blocks_simulator[blocks_index] += 1

        else:  # else we append a new block into the simulator and start adding the filled slots into it
            blocks_index += 1
            blocks_simulator.append(1)

    if blocks_simulator == blocks:
        return True
    return False


def get_intersection_row(rows):
    """Gets different rows and return the
    intersection between them"""
    result = list()  # storage for our intersection
    if len(rows) == 1:
        return rows[0]

    try:
        if WHITE_SLOTS not in rows[0] \
                and BLACK_SLOTS not in rows[0] \
                and EMPTY_SLOTS not in rows[0]:
            return []
    except:
        return []

    for j in range(len(rows[0])):  # loop over different rows
        checker = list()
        for i in range(len(rows)):  # loops over different arguments in each row

            if rows[i][j] == BLACK_SLOTS:  # if an argument is 1 in any row we add 1 to the intersection and break
                checker.append(BLACK_SLOTS)

            elif rows[i][j] == WHITE_SLOTS:  # if an argument is 0 in all row we add 0 to the intersection and break
                checker.append(WHITE_SLOTS)

        if checker.count(BLACK_SLOTS) == len(rows):
            result.append(BLACK_SLOTS)

        elif checker.count(WHITE_SLOTS) == len(rows):
            result.append(WHITE_SLOTS)

        else:
            result.append(EMPTY_SLOTS)
    return result  # returning the intersection


def solve_easy_nonogram(constraints):
    """returns an easy simply solution for
    a nonogram board by looking at the intersection
    of the constraints"""

    rows_constraints = constraints[0]  # separating the rows and the columns constraints
    columns_constraints = constraints[1]

    if check_for_columns_constraints(constraints):  # check for valid input
        if len(rows_constraints) == 0:
            return []

    board = draw_board(rows_constraints, columns_constraints)  # drawing an empty board
    return solve_easy_nonogram_helper(board, rows_constraints, columns_constraints)  # calling the help func


def check_for_columns_constraints(constraints):
    empty_list_check = 0  # checking for valid columns constraints
    for i in constraints[1]:
        if not i:
            empty_list_check += 1
    if empty_list_check == len(constraints[1]):
        return True


def solve_easy_nonogram_helper(board, rows_constraints, columns_constraints):
    """a helper function for the solve_easy_nonogram function"""
    copy_of_board = deepcopy(board)
    for row in range(len(rows_constraints)):  # looping over the rows constraints
        row_variations = get_row_variations(copy_of_board[row], rows_constraints[row])
        row_intersection = get_intersection_row(row_variations)
        copy_of_board[row] = row_intersection

    if type(copy_of_board[0]) == int():
        columns = make_columns([copy_of_board])  # turning the board into lists of columns
    else:
        columns = make_columns(copy_of_board)  # turning the board into lists of columns

    for column in range(len(columns_constraints)):  # looping over the columns constraints
        column_variations = get_row_variations(columns[column], columns_constraints[column])
        column_intersection = get_intersection_row(column_variations)
        append_column_to_board(column_intersection, copy_of_board, column)

    if board == copy_of_board:  # if no change was made then stop
        return copy_of_board
    elif [board] == copy_of_board:
        return copy_of_board

    else:  # else recursion
        return solve_easy_nonogram_helper(copy_of_board, rows_constraints, columns_constraints)


def append_column_to_board(column, board, column_idx):
    """appending the changes that was made on the
    columns to the board"""
    for i in range(len(column)):
        board[i][column_idx] = column[i]


def make_columns(board):
    """turning a board from a list of rows
    to a list of columns"""
    columns = []

    for arg in range(len(board[0])):
        column = []
        for row in range(len(board)):
            column.append(board[row][arg])

        columns.append(column)

    return columns


def draw_board(rows, columns):
    """Draws a board according to a given
    constraints"""
    board = list()
    for row in range(len(rows)):
        board.append([EMPTY_SLOTS] * len(columns))

    return board


def solve_nonogram(constraints):
    """returns a complete solution for a
    nonogram board ( if exists )"""

    solution = solve_easy_nonogram(constraints)

    for row in range(len(solution)):

        if solution[row].count(EMPTY_SLOTS) != 0:
            return []

    return [solution]


def count_row_variations(length, blocks, row=None):
    """Gets a length of a row and the blocks
    wants to fill and return the count of all the possible variations"""
    if not row:
        length -= (2 * len(blocks) - 2)

        result1 = fac(length + (len(blocks) - 1))
        result2 = fac(len(blocks)) * fac(length - 1)
        result = result1 / result2

        return int(result)

    else:
        return len(get_row_variations(row, blocks))



