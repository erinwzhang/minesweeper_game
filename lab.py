#!/usr/bin/env python3
"""6.009 Lab -- Six Double-Oh Mines"""

import typing
import doctest

# NO ADDITIONAL IMPORTS ALLOWED!


def dump(game):
    """
    Prints a human-readable version of a game (provided as a dictionary)
    """
    for key, val in sorted(game.items()):
        if isinstance(val, list) and val and isinstance(val[0], list):
            print(f'{key}:')
            for inner in val:
                print(f'    {inner}')
        else:
            print(f'{key}:', val)


# 2-D IMPLEMENTATION


def new_game_2d(num_rows, num_cols, bombs):
    """
    Start a new game.

    Return a game state dictionary, with the 'dimensions', 'state', 'board' and
    'visible' fields adequately initialized.

    Parameters:
       num_rows (int): Number of rows
       num_cols (int): Number of columns
       bombs (list): List of bombs, given in (row, column) pairs, which are
                     tuples

    Returns:
       A game state dictionary

    >>> dump(new_game_2d(2, 4, [(0, 0), (1, 0), (1, 1)]))
    board:
        ['.', 3, 1, 0]
        ['.', '.', 1, 0]
    dimensions: (2, 4)
    state: ongoing
    visible:
        [False, False, False, False]
        [False, False, False, False]
    """
    return new_game_nd((num_rows, num_cols), bombs)


def dig_2d(game, row, col):
    """
    Reveal the cell at (row, col), and, in some cases, recursively reveal its
    neighboring squares.

    Update game['visible'] to reveal (row, col).  Then, if (row, col) has no
    adjacent bombs (including diagonally), then recursively reveal (dig up) its
    eight neighbors.  Return an integer indicating how many new squares were
    revealed in total, including neighbors, and neighbors of neighbors, and so
    on.

    The state of the game should be changed to 'defeat' when at least one bomb
    is visible on the board after digging (i.e. game['visible'][bomb_location]
    == True), 'victory' when all safe squares (squares that do not contain a
    bomb) and no bombs are visible, and 'ongoing' otherwise.

    Parameters:
       game (dict): Game state
       row (int): Where to start digging (row)
       col (int): Where to start digging (col)

    Returns:
       int: the number of new squares revealed

    >>> game = {'dimensions': (2, 4),
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'visible': [[False, True, False, False],
    ...                  [False, False, False, False]],
    ...         'state': 'ongoing'}
    >>> dig_2d(game, 0, 3)
    4
    >>> dump(game)
    board:
        ['.', 3, 1, 0]
        ['.', '.', 1, 0]
    dimensions: (2, 4)
    state: victory
    visible:
        [False, True, True, True]
        [False, False, True, True]

    >>> game = {'dimensions': [2, 4],
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'visible': [[False, True, False, False],
    ...                  [False, False, False, False]],
    ...         'state': 'ongoing'}
    >>> dig_2d(game, 0, 0)
    1
    >>> dump(game)
    board:
        ['.', 3, 1, 0]
        ['.', '.', 1, 0]
    dimensions: [2, 4]
    state: defeat
    visible:
        [True, True, False, False]
        [False, False, False, False]

    >>> game = {'dimensions': [3, 5],
    ...         'board': [['.', 3, 1, 0, 0],
    ...                   ['.', '.', 1, 0, 0],
    ...                   [2, 2, 1, 0, 0]],
    ...         'visible': [[False, True, False, False, False],
    ...                  [False, False, False, False, False],
    ...                  [False, False, False, False, False]],
    ...         'state': 'ongoing'}
    >>> dig_2d(game, 1, 4)
    9
    """
    return dig_nd(game, (row, col))


def render_2d_locations(game, xray=False):
    """
    Prepare a game for display.

    Returns a two-dimensional array (list of lists) of '_' (hidden squares),
    '.' (bombs), ' ' (empty squares), or '1', '2', etc. (squares neighboring
    bombs).  game['visible'] indicates which squares should be visible.  If
    xray is True (the default is False), game['visible'] is ignored and all
    cells are shown.

    Parameters:
       game (dict): Game state
       xray (bool): Whether to reveal all tiles or just the ones allowed by
                    game['visible']

    Returns:
       A 2D array (list of lists)

    >>> render_2d_locations({'dimensions': (2, 4),
    ...         'state': 'ongoing',
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'visible':  [[False, True, True, False],
    ...                   [False, False, True, False]]}, False)
    [['_', '3', '1', '_'], ['_', '_', '1', '_']]

    >>> render_2d_locations({'dimensions': (2, 4),
    ...         'state': 'ongoing',
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'visible':  [[False, True, False, True],
    ...                   [False, False, False, True]]}, True)
    [['.', '3', '1', ' '], ['.', '.', '1', ' ']]
    """
    return render_nd(game, xray)
    

def render_2d_board(game, xray=False):
    """
    Render a game as ASCII art.

    Returns a string-based representation of argument 'game'.  Each tile of the
    game board should be rendered as in the function
        render_2d_locations(game)

    Parameters:
       game (dict): Game state
       xray (bool): Whether to reveal all tiles or just the ones allowed by
                    game['visible']

    Returns:
       A string-based representation of game

    >>> render_2d_board({'dimensions': (2, 4),
    ...                  'state': 'ongoing',
    ...                  'board': [['.', 3, 1, 0],
    ...                            ['.', '.', 1, 0]],
    ...                  'visible':  [[True, True, True, False],
    ...                            [False, False, True, False]]})
    '.31_\\n__1_'
    """
    locations = render_2d_locations(game, xray)
    board = ""
    for i in range(len(locations)):
        for j in range(len(locations[i])):
            board += locations[i][j]
        board += "\n"
    return board[:-1] # to remove extra new line


# N-D IMPLEMENTATION


def new_game_nd(dimensions, bombs):
    """
    Start a new game.

    Return a game state dictionary, with the 'dimensions', 'state', 'board' and
    'visible' fields adequately initialized.


    Args:
       dimensions (tuple): Dimensions of the board
       bombs (list): Bomb locations as a list of lists, each an
                     N-dimensional coordinate

    Returns:
       A game state dictionary

    >>> g = new_game_nd((2, 4, 2), [(0, 0, 1), (1, 0, 0), (1, 1, 1)])
    >>> dump(g)
    board:
        [[3, '.'], [3, 3], [1, 1], [0, 0]]
        [['.', 3], [3, '.'], [1, 1], [0, 0]]
    dimensions: (2, 4, 2)
    state: ongoing
    visible:
        [[False, False], [False, False], [False, False], [False, False]]
        [[False, False], [False, False], [False, False], [False, False]]
    """
    board = make_dimensional_list_nd(dimensions, 0) # board of all 0's
    visible = make_dimensional_list_nd(dimensions, False) # starts of all False

    # update each bomb's neighbors (that aren't bombs)
    for bomb in bombs:
        set_value(board, bomb, '.')
        for neighbor in get_neighbors(bomb):
            flag = True
            for i in range(len(dimensions)):
                if not (0 <= neighbor[i] < dimensions[i]): # out of range
                    flag = False
                    break
            if flag and get_value(board, neighbor) != '.':
                set_value(board, neighbor, get_value(board, neighbor)+1)
    
    return {
        'dimensions': dimensions,
        'board': board,
        'visible': visible,
        'state': 'ongoing'}


def make_dimensional_list_nd(dimensions, val):
    """
    Creates a list (of lists) of the proper dimensions filled with one val

    Parameters:
        dimensions (tuple): dimensions of list
        val: what to fill the lists with
    """
    array = []
    cur_dim = dimensions[0]
    new_dim = dimensions[1:]

    # base case: if no extra dimensions left, create the one dim list
    if len(new_dim) == 0:
        return [val for _ in range(cur_dim)]
    
    # else make a recursive call without the first dim
    array = [make_dimensional_list_nd(new_dim, val) for _ in range(cur_dim)]
    return array


def get_value(array, coord):
    """
    Recursively gets the value at a coordinate for an N-dimensional array
    """
    # base case: if down to a one-dimensional array
    if len(coord) == 1:
        return array[coord[0]]
    
    index = coord[0]
    coord = coord[1:]
    return get_value(array[index], coord)


def set_value(array, coord, val):
    """
    Recursively sets the value of a given 'array' at 'coord' to 'val'
    """
    # base case: if at one-dimensional array
    # all calls are still pointing at original array, so 'array' is properly updated
    if len(coord) == 1:
        array[coord[0]] = val
        return None
    
    index = coord[0]
    coord = coord[1:]
    return set_value(array[index], coord, val)


def get_neighbors(coord):
    """
    Recursively gets all possible neighbors of a coord
    Note: negative coordinates may be returned
    """
    neighbors = []

    # base case: if at one-dimensional array, get left and right
    if len(coord) == 1:
        return [(coord[0] + _,) for _ in range(-1, 2)]
    
    index = coord[-1] # must take elements off coord backwards due to append
    coord = coord[:-1]

    # recursive call to get_neighbors
    for n in get_neighbors(coord):
        for d in range(-1, 2):
            neighbors.append(n + (index + d,))
    return neighbors


def get_coords(dims):
    """
    Recursively gets all possible coordinates of an N-dimensional array given the dimensions
    """
    coords = []

    # base case: if down to one-dimensional array, start the tuple
    if len(dims) == 1:
        return [(i,) for i in range(dims[0])]

    dim = dims[0] # go forwards ('queue-like') so append at end works properly
    dims = dims[1:]
    for coord in get_coords(dims):
        for i in range(dim):
            coords.append((i,) + coord)
    return coords


def dig_nd(game, coordinates):
    """
    Recursively dig up square at coords and neighboring squares.

    Update the visible to reveal square at coords; then recursively reveal its
    neighbors, as long as coords does not contain and is not adjacent to a
    bomb.  Return a number indicating how many squares were revealed.  No
    action should be taken and 0 returned if the incoming state of the game
    is not 'ongoing'.

    The updated state is 'defeat' when at least one bomb is visible on the
    board after digging, 'victory' when all safe squares (squares that do
    not contain a bomb) and no bombs are visible, and 'ongoing' otherwise.

    Args:
       coordinates (tuple): Where to start digging

    Returns:
       int: number of squares revealed

    >>> g = {'dimensions': (2, 4, 2),
    ...      'board': [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...      'visible': [[[False, False], [False, True], [False, False],
    ...                [False, False]],
    ...               [[False, False], [False, False], [False, False],
    ...                [False, False]]],
    ...      'state': 'ongoing'}
    >>> dig_nd(g, (0, 3, 0))
    8
    >>> dump(g)
    board:
        [[3, '.'], [3, 3], [1, 1], [0, 0]]
        [['.', 3], [3, '.'], [1, 1], [0, 0]]
    dimensions: (2, 4, 2)
    state: ongoing
    visible:
        [[False, False], [False, True], [True, True], [True, True]]
        [[False, False], [False, False], [True, True], [True, True]]
    >>> g = {'dimensions': (2, 4, 2),
    ...      'board': [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...      'visible': [[[False, False], [False, True], [False, False],
    ...                [False, False]],
    ...               [[False, False], [False, False], [False, False],
    ...                [False, False]]],
    ...      'state': 'ongoing'}
    >>> dig_nd(g, (0, 0, 1))
    1
    >>> dump(g)
    board:
        [[3, '.'], [3, 3], [1, 1], [0, 0]]
        [['.', 3], [3, '.'], [1, 1], [0, 0]]
    dimensions: (2, 4, 2)
    state: defeat
    visible:
        [[False, True], [False, True], [False, False], [False, False]]
        [[False, False], [False, False], [False, False], [False, False]]
    """
    # refactored, game must be ongoing to click
    if game['state'] != 'ongoing':
        return 0
    
    # sad
    if get_value(game['visible'], coordinates) == True:
        return 0

    # if a bomb clicked, game is lost
    if get_value(game['board'], coordinates) == '.':
        set_value(game['visible'], coordinates, True)
        game['state'] = 'defeat'
        return 1

    def helper(game, coordinates):
        # removed check for if square already visible, as it won't be called recursively at all
        set_value(game['visible'], coordinates, True)
        revealed = 1

        if get_value(game['board'], coordinates) == 0:
            for neighbor in get_neighbors(coordinates):
                # check if each index of neighbor is in range
                flag = True
                for i in range(len(game['dimensions'])):
                    if not (0 <= neighbor[i] < game['dimensions'][i]): # out of range
                        flag = False
                        break
                if flag and get_value(game['board'], neighbor) != '.' and get_value(game['visible'], neighbor) == False:
                    revealed += helper(game, neighbor)
        return revealed

    revealed = helper(game, coordinates)

    # don't need else below
    if victory_check_nd(game):
        game['state'] = 'victory'
    
    return revealed

    
def victory_check_nd(game):
    """
    Checks if game has been won or not by traversing until a covered square is encountered
    """
    for coord in get_coords(game['dimensions']):
        if get_value(game['visible'], coord) == False and get_value(game['board'], coord) != '.':
            return False
    return True


def render_nd(game, xray=False):
    """
    Prepare the game for display.

    Returns an N-dimensional array (nested lists) of '_' (hidden squares), '.'
    (bombs), ' ' (empty squares), or '1', '2', etc. (squares neighboring
    bombs).  The game['visible'] array indicates which squares should be
    visible.  If xray is True (the default is False), the game['visible'] array
    is ignored and all cells are shown.

    Args:
       xray (bool): Whether to reveal all tiles or just the ones allowed by
                    game['visible']

    Returns:
       An n-dimensional array of strings (nested lists)

    >>> g = {'dimensions': (2, 4, 2),
    ...      'board': [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...      'visible': [[[False, False], [False, True], [True, True],
    ...                [True, True]],
    ...               [[False, False], [False, False], [True, True],
    ...                [True, True]]],
    ...      'state': 'ongoing'}
    >>> render_nd(g, False)
    [[['_', '_'], ['_', '3'], ['1', '1'], [' ', ' ']],
     [['_', '_'], ['_', '_'], ['1', '1'], [' ', ' ']]]

    >>> render_nd(g, True)
    [[['3', '.'], ['3', '3'], ['1', '1'], [' ', ' ']],
     [['.', '3'], ['3', '.'], ['1', '1'], [' ', ' ']]]
    """
    # create a copy board to modify
    board = make_dimensional_list_nd(game['dimensions'], None)
    for coord in get_coords(game['dimensions']):
        if xray or get_value(game['visible'], coord): # second condition means not xray
            if get_value(game['board'], coord) == 0:
                set_value(board, coord, ' ')
            else:
                set_value(board, coord, str(get_value(game['board'], coord)))
        else: # not xray and not visible
            set_value(board, coord, '_')
    
    return board


if __name__ == "__main__":
    # print(make_dimensional_list_nd((2, 3, 4), 0))
    # print(get_neighbors((5, 13, 0)))
    # board = [['.', 3, 1, 0],
    #         ['.', '.', 1, 0]]
    # set_value(board, (0, 0), 2)
    # print(board)
    # print(get_coords((3, 2, 1)))
    # Test with doctests. Helpful to debug individual lab.py functions.
    _doctest_flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    doctest.testmod(optionflags=_doctest_flags)  # runs ALL doctests

    # Alternatively, can run the doctests JUST for specified function/methods,
    # e.g., for render_2d_locations or any other function you might want.  To
    # do so, comment out the above line, and uncomment the below line of code.
    # This may be useful as you write/debug individual doctests or functions.
    # Also, the verbose flag can be set to True to see all test results,
    # including those that pass.
    #
    # doctest.run_docstring_examples(
    #    render_2d_locations,
    #    globals(),
    #    optionflags=_doctest_flags,
    #    verbose=False
    # )







# CHANGED FUNCTIONS
# def new_game_2d(num_rows, num_cols, bombs):
#     """
#     Start a new game.

#     Return a game state dictionary, with the 'dimensions', 'state', 'board' and
#     'visible' fields adequately initialized.

#     Parameters:
#        num_rows (int): Number of rows
#        num_cols (int): Number of columns
#        bombs (list): List of bombs, given in (row, column) pairs, which are
#                      tuples

#     Returns:
#        A game state dictionary

#     >>> dump(new_game_2d(2, 4, [(0, 0), (1, 0), (1, 1)]))
#     board:
#         ['.', 3, 1, 0]
#         ['.', '.', 1, 0]
#     dimensions: (2, 4)
#     state: ongoing
#     visible:
#         [False, False, False, False]
#         [False, False, False, False]
#     """
#     # combined board and visible makers into one helper function, looping through just once
#     board, visible = make_starter_board_visible_2d(num_rows, num_cols, bombs)
#     board = count_bombs_2d(board, num_rows, num_cols) # refactoring away from manual checks at each index
#     return {
#         'dimensions': (num_rows, num_cols),
#         'board': board,
#         'visible': visible,
#         'state': 'ongoing'}


# def make_starter_board_visible_2d(num_rows, num_cols, bombs):
#     """
#     Creates a board and visible list of lists

#     Parameters:
#         num_rows (int): Number of rows
#         num_cols (int): Number of columns
#         bombs (list): List of bomb coordinates

#     Returns:
#         board, a list of lists with '.' at bomb locations and 0 everywhere else
#         visible, a list of lists of bools starting out as False
#     """
#     board = []
#     visible = []
#     for r in range(num_rows):
#         row_b = []
#         row_v = []
#         for c in range(num_cols):
#             row_v.append(False)
#             if [r, c] in bombs or (r, c) in bombs:
#                 row_b.append('.')
#             else:
#                 row_b.append(0)
#         board.append(row_b)
#         visible.append(row_v)
#     return board, visible


# def count_bombs_2d(raw_board, num_rows, num_cols):
#     """
#     Updates a board with the correct number of bombs to remove manual checks at all surrounding indices

#     Parameters:
#         raw_board (list of lists): Filled with either 0 or '.'
#         num_rows (int): Number of rows
#         num_cols (int): Number of columns

#     Returns:
#         An updated board with the correct number of bombs
#     """
#     for r in range(num_rows):
#         for c in range(num_cols):
#             if raw_board[r][c] == 0: # not a bomb
#                 neighbor_bombs = 0
#                 for i in range(-1, 2):
#                     for j in range(-1, 2):
#                         if 0 <= r+i < num_rows and 0 <= c+j < num_cols: # check if in range
#                             if raw_board[r+i][c+j] == '.':
#                                 neighbor_bombs += 1
#                 raw_board[r][c] = neighbor_bombs
#     return raw_board


# def dig_2d(game, row, col):
#     """
#     Reveal the cell at (row, col), and, in some cases, recursively reveal its
#     neighboring squares.

#     Update game['visible'] to reveal (row, col).  Then, if (row, col) has no
#     adjacent bombs (including diagonally), then recursively reveal (dig up) its
#     eight neighbors.  Return an integer indicating how many new squares were
#     revealed in total, including neighbors, and neighbors of neighbors, and so
#     on.

#     The state of the game should be changed to 'defeat' when at least one bomb
#     is visible on the board after digging (i.e. game['visible'][bomb_location]
#     == True), 'victory' when all safe squares (squares that do not contain a
#     bomb) and no bombs are visible, and 'ongoing' otherwise.

#     Parameters:
#        game (dict): Game state
#        row (int): Where to start digging (row)
#        col (int): Where to start digging (col)

#     Returns:
#        int: the number of new squares revealed

#     >>> game = {'dimensions': (2, 4),
#     ...         'board': [['.', 3, 1, 0],
#     ...                   ['.', '.', 1, 0]],
#     ...         'visible': [[False, True, False, False],
#     ...                  [False, False, False, False]],
#     ...         'state': 'ongoing'}
#     >>> dig_2d(game, 0, 3)
#     4
#     >>> dump(game)
#     board:
#         ['.', 3, 1, 0]
#         ['.', '.', 1, 0]
#     dimensions: (2, 4)
#     state: victory
#     visible:
#         [False, True, True, True]
#         [False, False, True, True]

#     >>> game = {'dimensions': [2, 4],
#     ...         'board': [['.', 3, 1, 0],
#     ...                   ['.', '.', 1, 0]],
#     ...         'visible': [[False, True, False, False],
#     ...                  [False, False, False, False]],
#     ...         'state': 'ongoing'}
#     >>> dig_2d(game, 0, 0)
#     1
#     >>> dump(game)
#     board:
#         ['.', 3, 1, 0]
#         ['.', '.', 1, 0]
#     dimensions: [2, 4]
#     state: defeat
#     visible:
#         [True, True, False, False]
#         [False, False, False, False]

#     >>> game = {'dimensions': [3, 5],
#     ...         'board': [['.', 3, 1, 0, 0],
#     ...                   ['.', '.', 1, 0, 0],
#     ...                   [2, 2, 1, 0, 0]],
#     ...         'visible': [[False, True, False, False, False],
#     ...                  [False, False, False, False, False],
#     ...                  [False, False, False, False, False]],
#     ...         'state': 'ongoing'}
#     >>> dig_2d(game, 1, 4)
#     9
#     """
    
#     # check if ongoing instead of if victory or defeat
#     if game['state'] != 'ongoing':
#         # removed the line keeping the state the same
#         return 0

#     if game['visible'][row][col]] == True:
#         return 0

#     if game['board'][row][col] == '.':
#         game['visible'][row][col] = True
#         game['state'] = 'defeat'
#         return 1

#     # deleted excess covered_squares, then victory, check

#     def helper(game, row, col):
#         removed check for if square already visible, as it won't be called recursively at all
#         game['visible'][row][col] = True
#         revealed = 1

#         # refactoring of manual checks
#         if game['board'][row][col] == 0:
#             num_rows, num_cols = game['dimensions']
#             for i in range(-1, 2):
#                 for j in range(-1, 2):
#                     if 0 <= row+i < num_rows and 0 <= col+j < num_cols: # check if in rang
#                         if game['board'][row+i][col+j] != '.' and game['visible'][row+i][col+j] == False:
#                             revealed += helper(game, row+i, col+j)
#         return revealed

#     revealed = helper(game, row, col)

#     # did a victory check instead of looping through the whole game
#     # since covered_squares only exists for a victory check
#     if victory_check_2d(game):
#         game['state'] = 'victory'
    
#     # moved return statement out of check for dry-ness
#     # then ended up deleting the else altogether, since state is already ongoing
#     return revealed


# def victory_check_2d(game):
#     """
#     Formerly:
#       Counts how many covered squares still exist in the game
#       Refactoring: removed the check for number of visible bombs
#     Currently: stops and returns False once a covered square is found
#     """
#     for r in range(game['dimensions'][0]):
#         for c in range(game['dimensions'][1]):
#             if game['visible'][r][c] == False and game['board'][r][c] != '.':
#                 return False
#     return True


# def render_2d_locations(game, xray=False):
#     """
#     Prepare a game for display.

#     Returns a two-dimensional array (list of lists) of '_' (hidden squares),
#     '.' (bombs), ' ' (empty squares), or '1', '2', etc. (squares neighboring
#     bombs).  game['visible'] indicates which squares should be visible.  If
#     xray is True (the default is False), game['visible'] is ignored and all
#     cells are shown.

#     Parameters:
#        game (dict): Game state
#        xray (bool): Whether to reveal all tiles or just the ones allowed by
#                     game['visible']

#     Returns:
#        A 2D array (list of lists)

#     >>> render_2d_locations({'dimensions': (2, 4),
#     ...         'state': 'ongoing',
#     ...         'board': [['.', 3, 1, 0],
#     ...                   ['.', '.', 1, 0]],
#     ...         'visible':  [[False, True, True, False],
#     ...                   [False, False, True, False]]}, False)
#     [['_', '3', '1', '_'], ['_', '_', '1', '_']]

#     >>> render_2d_locations({'dimensions': (2, 4),
#     ...         'state': 'ongoing',
#     ...         'board': [['.', 3, 1, 0],
#     ...                   ['.', '.', 1, 0]],
#     ...         'visible':  [[False, True, False, True],
#     ...                   [False, False, False, True]]}, True)
#     [['.', '3', '1', ' '], ['.', '.', '1', ' ']]
#     """
#     # code is kind of wet (not DRY) sorry :(
#     locations = []
#     if xray:
#         for i in range(len(game['board'])):
#             locations.append([' ' if game['board'][i][j] == 0 else str(game['board'][i][j]) for j in range(len(game['board'][i]))])
#         return locations

#     for i in range(len(game['board'])):
#         row = []
#         for j in range(len(game['board'][i])):
#             if game['visible'][i][j]:
#                 if game['board'][i][j] == 0:
#                     row.append(' ')
#                 else:
#                     row.append(str(game['board'][i][j]))
#             else:
#                 row.append('_')
#         locations.append(row)
#     return locations