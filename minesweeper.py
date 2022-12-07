import random
import re
# board object to represent minesweeper game
# this is so that we can just say "create a new board object", or
# "dig here", or "render this game for this object"
class Board:
    def __init__(self, dim_size,num_bombs):
        #let's keep track of these parameters. they'll be helpful later
        self.dim_size = dim_size
        self.num_bombs = num_bombs

        # create the board
        #helper function
        self.board = self.make_new_board()
        self.assign_values_to_board()

        #initialize a set to keep track of which locations we've uncovered
        #we'll save (row,col) tuples into this set
        self.dug = set() # if we dig at 0, 0, then self.dug = {(0,0)}

    def make_new_board(self):
        # construct a new board based on the dim size of num bombs
        # we should construct the list of lists here (o whatever representation you prefer,
        # but since we have a 2-D board, list of lists is most natural)

        #generate a new board
        board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]
        print
        #this creates an array like this
        #[None, None, None, None],
        #[None, None, None, None],

        #plant the bombs
        bombs_planted = 0
        while bombs_planted < self.num_bombs:
            loc = random.randint(0, self.dim_size**2 - 1) # return a random integer N such that a <= N <= b
            row = loc // self.dim_size # number of times dim_size is divisible by loc is the row
            col = loc % self.dim_size # remainder equals the column

            if board[row][col] == "*":
                # this means we've already planted a bomb
                continue
            board[row][col] = "*" # plant the bomb
            bombs_planted += 1

        return board

    def assign_values_to_board(self):
        #with bombs planted, we assign 0-8 to all empty spaces, which represents neighboring bombs
        #we precompute these to save effort later
        for r in range(self.dim_size):
            for c in range(self.dim_size):
                if self.board[r][c] == "*":
                     #if this is already a bomb, skip it
                     continue
                self.board[r][c] = self.get_num_neighboring_bombs(r, c)
    
    def get_num_neighboring_bombs(self, row, col):
        # iterate through each neighboring position and sum number of bombs
        # top left: (row-1, col-1)
        # top middle: (row-1, col)
        # top right: (row-1, col+1)
        # left: (row, col-1)
        # right: (row, col+1)
        # bottom left: (row+1, col-1)
        # bottom middle: (row+1, col)
        # bottom right: (row+1, col+1) 
        # make sure not to go out of bounds

        num_neighboring_bombs = 0 
        for r in range(max(0, row-1), min(self.dim_size-1, row+1)+1):
            for c in range(max(0, col-1), min(self.dim_size-1, col+1)+1):
                if r == row and c == col:
                    #original location, don't check
                    continue
                if self.board[r][c] == "*":
                    num_neighboring_bombs += 1
        
        return num_neighboring_bombs

    def dig(self, row, col):
        #dig at that location!
        #return True if successful dig, False if bomb dug

        # fit bomb = game over
        # location with neighboring bombs = finish dig
        # dig at location with no neighboring bombs = recursively dig neighbors

        self.dug.add((row,col)) # keep track of dig sites
        
        if self.board[row][col] == "*":
            return False
        elif self.board[row][col] > 0: #location with neighboring bombs
            return True

        for r in range(max(0, row-1), min(self.dim_size-1, row+1)+1):
            for c in range(max(0, col-1), min(self.dim_size-1, col+1)+1):
                if (r, c) in self.dug:
                    continue # dont dig where you already have
                self.dig(r, c)
        # if initial dig didn't hit a bomb, we *shouldnt* hit a bomb here
        return True

    def __str__(self):
        #this is a function where, if you call print on this object,
        #it will print wout what this function returns!
        #return a string that shows the board to the player

        # first lets create a new array that represents what the user would see
        visible_board = [[None for _ in range(self.dim_size)] for _ in range (self.dim_size)]
        for row in range(self.dim_size):
            for col in range(self.dim_size):
                if (row, col) in self.dug:
                    visible_board[row][col] = str(self.board[row][col])
                else:
                    visible_board[row][col] = " "

        #put this together in a string
        string_rep = ''
        # get max column widths for printing
        widths = []
        for idx in range(self.dim_size):
            columns = map(lambda x: x[idx], visible_board)
            widths.append(
                len(
                    max(columns, key = len)
                )
            )

        # print the csv strings
        indices = [i for i in range(self.dim_size)]
        indices_row = '   '
        cells = []
        for idx, col in enumerate(indices):
            format = '%-' + str(widths[idx]) + "s"
            cells.append(format % (col))
        indices_row += '  '.join(cells)
        indices_row += '  \n'
        
        for i in range(len(visible_board)):
            row = visible_board[i]
            string_rep += f'{i} |'
            cells = []
            for idx, col in enumerate(row):
                format = '%-' + str(widths[idx]) + "s"
                cells.append(format % (col))
            string_rep += ' |'.join(cells)
            string_rep += ' |\n'

        str_len = int(len(string_rep) / self.dim_size)
        string_rep = indices_row + '-'*str_len + '\n' + string_rep + '-'*str_len

        return string_rep



def play(dim_size=10, num_bombs=10):
    #step 1: create the board and plant the bombs
    board = Board(dim_size, num_bombs)
    #step 2:show the user the board and ask for where they want to dig
    #step 3a: if location is a bomb, show game over message
    #step 3b: if location is not a bomb, dig recursively until each square
            # us at least next to a bomb
    #step 4: repeat steps 2 and 3a/b until there are no more places to dig -> Victory!
    safe = True
    while len(board.dug) < board.dim_size **2 - num_bombs:
        print(board)
        # 0,0 or 0, 0 or 0,    0 splits the string at the comma and spaces (\\s)* detects any number of spaces
        user_input = re.split(",(\\s)*", input("Where would you like to dig? Input as row, col: ")) # "0, 3", 
        row, col = int(user_input[0]), int(user_input[-1])
        if row < 0 or row >= board.dim_size or col < 0 or col>= dim_size:
            print("Invalid location.Try again.")
            continue
        #if valid we dig
        safe = board.dig(row, col)
        if not safe:
            #dug a bomb
            break

    # 2 ways to end loop
    if safe:
        print("Congratulations, you are victorious!")
    else:
        print("Sorry game over, you blew up...")
        #reveal the board
        board.dug = [(r, c) for r in range(board.dim_size) for c in range(board.dim_size)]
        print(board)

if __name__ == "__main__": #good practice
    play()