import math, random
import copy
import pygame
import sys

"""
This was adapted from a GeeksforGeeks article "Program for Sudoku Generator" by Aarti_Rathi and Ankur Trisal
https://www.geeksforgeeks.org/program-sudoku-generator/

"""


class SudokuGenerator:
    '''
	create a sudoku board - initialize class variables and set up the 2D board
	This should initialize:
	self.row_length		- the length of each row
	self.removed_cells	- the total number of cells to be removed
	self.board			- a 2D list of ints to represent the board
	self.box_length		- the square root of row_length

	Parameters:
    row_length is the number of rows/columns of the board (always 9 for this project)
    removed_cells is an integer value - the number of cells to be removed

	Return:
	None
    '''

    def __init__(self, row_length, removed_cells):
        self.row_length = row_length
        self.removed_cells = removed_cells
        self.box_length = int(row_length ** 0.5)
        self.board_blank = [[0 for i in range(self.row_length)] for i in range(self.row_length)]
        self.board = copy.deepcopy(self.board_blank)  # active player board ***TEMPORARILY**** Blank
        self.fill_diagonal()
        self.fill_remaining(0, 0)
        self.board_correct = copy.deepcopy(self.board)  # used to see if matches correct answer
        self.remove_cells()
        self.board_original = copy.deepcopy(
            self.board)  # used to see where valid player inputs are and the og board with spots removed

        '''
	Returns a 2D python list of numbers which represents the board

	Parameters: None
	Return: list[list]
    '''

    def get_board(self):
        return self.board

    '''
	Displays the board to the console
    This is not strictly required, but it may be useful for debugging purposes

	Parameters: None
	Return: None
    '''

    def print_board(self):
        for i in range(self.row_length):
            print(self.board[i])

    '''
	Determines if num is contained in the specified row (horizontal) of the board
    If num is already in the specified row, return False. Otherwise, return True

	Parameters:
	row is the index of the row we are checking
	num is the value we are looking for in the row

	Return: boolean
    '''

    def valid_in_row(self, row, num):
        if num in self.board[row]:  # check if num in the row, and the nested lists within that row
            return False  # this is not allowed
        return True  # didn't find a problem

    '''
	Determines if num is contained in the specified column (vertical) of the board
    If num is already in the specified col, return False. Otherwise, return True

	Parameters:
	col is the index of the column we are checking
	num is the value we are looking for in the column

	Return: boolean
    '''

    def valid_in_col(self, col, num):
        for i in range(
                9):  # iterate through the 9 rows(non inclusive bc indexing is 0-8). For below, i subtract one for same reason of list indexing starting at 0
            if self.board[i][
                col] == num:  # this works but calls wrong variable, the third index is computed that way because -1 gives the index and the 3* and //3 gives the index in the nested list
                return False  # this is not a valid move
        return True  # never found the num thus this is allowed

    '''
	Determines if num is contained in the 3x3 box specified on the board
    If num is in the specified box starting at (row_start, col_start), return False.
    Otherwise, return True

	Parameters:
	row_start and col_start are the starting indices of the box to check
	i.e. the box is from (row_start, col_start) to (row_start+2, col_start+2)
	num is the value we are looking for in the box

	Return: boolean
    '''

    def valid_in_box(self, row_start, col_start, num):
        for row in range(row_start, row_start + 3):
            for col in range(col_start, col_start + 3):
                if self.board[row][col] == num:
                    return False
        return True

    '''
       Determines if it is valid to enter num at (row, col) in the board
       This is done by checking that num is unused in the appropriate, row, column, and box

       Parameters:
       row and col are the row index and col index of the cell to check in the board
       num is the value to test if it is safe to enter in this cell

       Return: boolean
       '''

    def is_valid(self, row, col, num):
        if not self.valid_in_col(col, num):
            return False
        elif not self.valid_in_row(row, num):
            return False
        elif not self.valid_in_box(3 * (row // 3), 3 * (col // 3), num):
            return False
        else:
            return True

    '''
    Fills the specified 3x3 box with values
    For each position, generates a random digit which has not yet been used in the box

	Parameters:
	row_start and col_start are the starting indices of the box to check
	i.e. the box is from (row_start, col_start) to (row_start+2, col_start+2)

	Return: None
    '''

    def fill_box(self, row_start, col_start):
        for row in range(row_start, row_start + 3):
            for col in range(col_start, col_start + 3):  # iterations
                while True:  # generate new terms until it is a valid addition
                    term = random.randrange(1, 10)
                    if self.is_valid(row, col, term):
                        self.board[row][col] = term
                        break  # if its valid put it in then break

    '''
    Fills the three boxes along the main diagonal of the board
    These are the boxes which start at (0,0), (3,3), and (6,6)

	Parameters: None
	Return: None
    '''

    def fill_diagonal(self):
        for i in range(3):
            self.fill_box(i * 3, i * 3)

    '''
    DO NOT CHANGE
    Provided for students
    Fills the remaining cells of the board
    Should be called after the diagonal boxes have been filled

	Parameters:
	row, col specify the coordinates of the first empty (0) cell

	Return:
	boolean (whether or not we could solve the board)
    '''

    def fill_remaining(self, row, col):
        if (col >= self.row_length and row < self.row_length - 1):
            row += 1
            col = 0
        if row >= self.row_length and col >= self.row_length:
            return True
        if row < self.box_length:
            if col < self.box_length:
                col = self.box_length
        elif row < self.row_length - self.box_length:
            if col == int(row // self.box_length * self.box_length):
                col += self.box_length
        else:
            if col == self.row_length - self.box_length:
                row += 1
                col = 0
                if row >= self.row_length:
                    return True

        for num in range(1, self.row_length + 1):
            if self.is_valid(row, col, num):
                self.board[row][col] = num
                if self.fill_remaining(row, col + 1):
                    return True
                self.board[row][col] = 0
        return False

    '''
    DO NOT CHANGE
    Provided for students
    Constructs a solution by calling fill_diagonal and fill_remaining

	Parameters: None
	Return: None
    '''

    def fill_values(self):
        self.fill_diagonal()
        self.fill_remaining(0, self.box_length)

    '''
    Removes the appropriate number of cells from the board
    This is done by setting some values to 0
    Should be called after the entire solution has been constructed
    i.e. after fill_values has been called

    NOTE: Be careful not to 'remove' the same cell multiple times
    i.e. if a cell is already 0, it cannot be removed again

	Parameters: None
	Return: None
    '''

    def remove_cells(self):
        past_cords = []
        for i in range(0, self.removed_cells):
            while True:
                row = random.randrange(0, 9)
                col = random.randrange(0, 9)
                if [row, col] not in past_cords:
                    past_cords += [row, col]
                    self.board[row][col] = 0
                    break


'''
DO NOT CHANGE
Provided for students
Given a number of rows and number of cells to remove, this function:
1. creates a SudokuGenerator
2. fills its values and saves this as the solved state
3. removes the appropriate number of cells
4. returns the representative 2D Python Lists of the board and solution

Parameters:
size is the number of rows/columns of the board (9 for this project)
removed is the number of cells to clear (set to 0)

Return: list[list] (a 2D Python list to represent the board)
'''


def generate_sudoku(size, removed):
    sudoku = SudokuGenerator(size, removed)
    sudoku.fill_values()
    board = sudoku.get_board()
    sudoku.remove_cells()
    board = sudoku.get_board()
    return board


def draw_grid(screen):
    for i in range(10):  # 10 lines to make a 9x9 grid
        width = 2 if i % 3 == 0 else 1  # Thicker lines for box boundaries
        pygame.draw.line(screen, (0, 0, 0), (i * 100, 0), (i * 100, 900), width)  # Vertical lines
        pygame.draw.line(screen, (0, 0, 0), (0, i * 100), (900, i * 100), width)  # Horizontal lines

# Function to place numbers on the board
def draw_numbers(screen, board):
    font = pygame.font.Font(None, 60)  # Font for numbers
    for row in range(9):
        for col in range(9):
            if board[row][col] != 0:  # Only display non-zero cells
                number = font.render(str(board[row][col]), True, (0, 0, 0))
                screen.blit(number, (col * 100 + 35, row * 100 + 25))  # Center numbers in cells


def main():
    pygame.init()
    screen = pygame.display.set_mode((900, 900))
    pygame.display.set_caption("Sudoku")
    screen.fill("light blue")

    # Generate the Sudoku board
    sudoku = SudokuGenerator(9, 20)  # 20 cells removed for the puzzle
    board = sudoku.get_board()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Clear the screen, draw grid, and numbers
        screen.fill("light blue")
        draw_grid(screen)
        draw_numbers(screen, board)

        pygame.display.update()

if __name__ == "__main__":
    main()



# x = SudokuGenerator(9, 0)
# x.print_board()
