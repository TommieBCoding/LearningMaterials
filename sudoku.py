def find_next_empty(puzzle):
    # finds the next row, col on the puzzle that's not filled yet, represented by -1
    # return row, col tuple (or (None,None) if there is none)

    #using 0-8 for indicies
    for r in range(9):
        for c in range(9): #range(9) is 0-8
            if puzzle[r][c] == -1:
                return r,c
    
    return None, None # if there are no empty spaces

def is_valid(puzzle, guess, row, col):
    # figures out whether the guess is valid
    # returns True if it is valid, false otherise

    #first the row
    row_vals = puzzle[row]
    if guess in row_vals:
        return False
    
    #then the column
    col_vals = [puzzle[i][col] for i in range(9)]
    if guess in col_vals:
        return False
    
    #finally the square
    # this is tricky, we want to get where the 3x3 square starts
    # and iterate over the 3 values in the row/column
    row_start = (row // 3) * 3 # how many times current index goes into 3 is our square order, 
    col_start = (col // 3) * 3 # multiply by 3 to get index of first place on square
    
    for r in range(row_start, row_start + 3):
        for c in range(col_start, col_start + 3):
            if puzzle[r][c] == guess:
                return False

    # if we get here, these checks pass
    return True
   

def solve_sudoku(puzzle):
    #solve sudoku using backtracking!
    # our puzzle is a list of lists, where each inner list is a row in our sudoku puzzle
    # return whether a solution exisists
    # mutates puzzle to be the solution

    #step 1: choose somewhere on the puzzle to make a guess
    row, col = find_next_empty(puzzle)

    # step 1.1 : If nowhere left, we are done
    if row is None:
        return True
    
    # step 2: if there is a space, make a guess between 1 and 9
    for guess in range(1, 10):
        #step 3: check if this is a valid guess
        if is_valid(puzzle, guess, row, col):
            #step 3.1: if this is valid, then place that guess on the puzzle!
            puzzle[row][col] = guess
            # now recurse using this puzzle!
            # step 4: recursively call our function
            if solve_sudoku(puzzle):
                return True

        # step 5: if not valid Or if our guess does not solve the puzzle, backtrack, try again
        puzzle[row][col] = -1

    #step 6: if none of the numbers we try work, then this is unsolvable
    return False

if __name__ == '__main__':
    example_board = [
        [9, 1, 3,   4, 2, 7,   -1, 8, -1],
        [6, -1, -1,   -1, -1, -1,   -1, -1, -1],
        [2, -1, -1,   -1, 1, 3,   -1, 7, -1],

        [-1, -1, -1,   1, -1, 2,   -1, -1, 8],
        [-1, 6, 2,   5, -1, -1,   -1, -1, 3],
        [5, 3, 8,   7, -1, -1,   2, 9, -1],

        [3, 4, -1,   8, 7, -1,   -1, 6, -1],
        [-1, -1, 6,   -1, 4, 9,   8, 1, 5],
        [8, -1, 1,   2, -1, -1,   -1, -1, -1]
    ]
    print(solve_sudoku(example_board))
    print(example_board)
