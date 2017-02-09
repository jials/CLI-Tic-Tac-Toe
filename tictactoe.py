from itertools import product
import getopt
import sys

SYMBOLS = ['x', 'o']
CHECK_X = [[-1, 1], [-1, 1], [-1, 1], [0, 0]]  # check diagonal, vertical, back diagonal and horizontal
CHECK_Y = [[-1, 1], [0, 0], [1, -1], [-1, 1]]
FIRST_PLAYER = 0
SECOND_PLAYER = 1


def init_board(size):
    board = {}
    for x, y in product(range(size), range(size)):
        board[(x, y)] = 0
    return board


def print_board(board, size):
    for grid in board:
        x, y = grid
        # new row
        if x != 0 and y == 0:
            dash_count = size * 4 - 1
            print('\n' + '-' * dash_count)

        val = board[grid]
        if val == 0:
            # starts from 1
            pos = int(x * size + y + 1)
            output = ' {:d} {bar}'.format(pos, bar='|' if y != size - 1 else '')
            print(output, end='')
        else:
            output = ' {} {bar}'.format(val, bar='|' if y != size - 1 else '')
            print(output, end='')
    print('\n')


def place_piece(board, size, pick, turn):
    # 1-based indexing
    x = (pick - 1) // size
    y = (pick - 1) % size

    if (x, y) in board.keys() and board[(x, y)] == 0:
        board[(x, y)] = SYMBOLS[turn]
        return True
    else:
        return False


def flip(n):
    return 1 - n


def check_victory(board, size, player_symbol):
    """
    Check every non-border grid to see if it satisfies the win condition

    :param board: the current board state
    :param size: size of the board
    :param player_symbol: the current player selected
    :return: True if the player wins, else False
    """
    for x, y in product(range(1, size - 1), range(1, size - 1)):
        # only 4 possible winning condition
        for i in range(4):
            if board[(x, y)] == player_symbol and board[(x, y)] == \
                    board[(x + CHECK_X[i][0], y + CHECK_Y[i][0])] == board[(x + CHECK_X[i][1], y + CHECK_Y[i][1])]:
                return True
    return False


def is_full(board):
    return all(x != 0 for x in board.values())


def find_winner(board, size):
    if check_victory(board, size, SYMBOLS[FIRST_PLAYER]):
        return FIRST_PLAYER
    elif check_victory(board, size, SYMBOLS[SECOND_PLAYER]):
        return SECOND_PLAYER
    elif is_full(board):
        return -1


def check_end(board, size):
    return check_victory(board, size, SYMBOLS[FIRST_PLAYER]) or check_victory(board, size, SYMBOLS[SECOND_PLAYER]) or is_full(board)


def usage():
    print("usage: " + sys.argv[0] + " -s <board_size>")


def main():
    size = None
    try:
        opts, args = getopt.getopt(sys.argv[1:], 's:')
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    for o, a in opts:
        if o == '-s':
            size = int(a)
        else:
            assert False, "unhandled option"

    if size is None:
        print("Size is not set! Default to size 3")
        print("To specify the size, run it as following:")
        usage()
        size = 3

    board = init_board(size)

    players = []
    player1 = input('Enter name for Player 1:\n')
    players.append(player1)

    player2 = input('Enter name for Player 2:\n')
    players.append(player2)

    turn = 0

    while not check_end(board, size):
        print('\n')
        print_board(board, size)
        pick = int(input('%s , choose a box to place an \'%s\' into: ' % (players[turn], SYMBOLS[turn])))

        if place_piece(board, size, pick, turn):
            print_board(board, size)
            turn = flip(turn)
        else:
            print("Invalid Input. Try Again!")

    winner = find_winner(board, size)
    if winner == -1:
        print('IT IS A TIE!')
    else:
        print('Congratulations %s! You have won.' % (players[winner]))

if __name__ == '__main__':
    main()
