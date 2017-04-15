rows = 'ABCDEFGHI'
cols = '123456789'

def cross(a, b):
    "Cross product of elements in A and elements in B."
    return [s+t for s in a for t in b]

boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
diagonal_units = [
    ['A1', 'B2', 'C3', 'D4', 'E5', 'F6', 'G7', 'H8', 'I9'],
    ['A9', 'B8', 'C7', 'D6', 'E5', 'F4', 'G3', 'H2', 'I1']
]
unitlist = row_units + column_units + square_units + diagonal_units

units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

assignments = []

def grid_values(grid):
    """Convert grid string into {<box>: <value>} dict with '.' value for empties.

    Args:
        grid: Sudoku grid in string form, 81 characters long
    Returns:
        Sudoku grid in dictionary form:
        - keys: Box labels, e.g. 'A1'
        - values: Value in corresponding box, e.g. '8', or '.' if it is empty.
    """
    return dict(zip(boxes, [cols if c == '.' else c for c in grid]))
def naked_twins(values):
    """Eliminate values using the naked twins strategy.

    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}
    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    for box, value in values.items():

        potential_twin_found = len(value) == 2
        if potential_twin_found:
            peer_units = units[box]

            # unit by unit, look for another twin
            for unit in peer_units:
                twin = next((peer for peer in unit if values[peer] == value and peer != box), False)
                if not twin:
                    continue

                # eg: ['A1', 'C1'], both equal '27'
                twins = [box, twin]
                unsolved_peers_list = [peer for peer in unit if peer not in twins and len(values[peer]) > 1]
                values = prune_twins_values_from_peers(values, unsolved_peers_list, twins, value)
    return values

def prune_twins_values_from_peers(values, peer_list, twins, twins_value):
    """Eliminate twins values from peers in the same unit.

    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}
        peer_list(array): peers of the naked twins
        twins(array): an array of naked twins
        twins_value(string): the naked twins value
    Returns:
        the values dictionary w/ current unit pruned via naked twins strategy
    """
    a, b = list(twins_value)
    for peer in peer_list:
        if a in values[peer]:
            values[peer] = values[peer].replace(a, '')
        if b in values[peer]:
            values[peer] = values[peer].replace(b, '')
    return values


def eliminate(values):
    """Eliminate values from peers of each box with a single value.

    Go through all the boxes, and whenever there is a box with a single value,
    eliminate this value from the set of values of all its peers.

    Args:
        values: Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after eliminating values.
    """
    for k, v in values.items():
        if len(v) == 1:
            for peer_key in peers[k]:
                values[peer_key] = values[peer_key].replace(v, '')
    return values

def only_choice(values):
    """Finalize all values that are the only choice for a unit.

    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.

    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after filling in only choices.
    """
    for unit in unitlist:
        for c in cols:
            result = list(filter((lambda x: c in values[x]), unit))
            if len(result) == 1:
                values[result[0]] = c
    return values

def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        values = eliminate(values)
        values = only_choice(values)
        values = naked_twins(values)

        assign_values(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    "Using depth-first search and propagation, create a search tree and solve the sudoku."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)

    if values is False: return False

    solved = all(len(values[box]) == 1 for box in boxes)
    if solved:
        return values

    (length, box) = min((len(values[box]), box) for box in boxes if len(values[box]) > 1)
    for c in values[box]:
        possible_sudoku = values.copy()
        possible_sudoku[box] = c
        play_through = search(possible_sudoku)
        if play_through: return play_through

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = grid_values(grid)
    assignments.append(values.copy())

    return search(values)

def assign_values(values):
    "Update the assignments list, given the last puzzle reduction"
    for box, value in values.items():
        assign_value(assignments[-1], box, value)

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    # seed assignments with initial board state
    if not assignments:
        assignments.append(values.copy())

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def display(values):
    """
    Display the values as a 2-D grid.
    Input: The sudoku in dictionary form
    Output: None
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return
if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
