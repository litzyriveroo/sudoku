import math, random
import copy
import pygame
import sys

from pygame.event import set_keyboard_grab

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
                    past_cords.append([row, col])
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
        if i == 0: # Thicker lines for box boundaries
            width = 1
        elif i % 3 == 0:
            width = 3
        else:
            width = 1
        # width = 3 if i % 3 == 0 else 1
        pygame.draw.line(screen, (0, 0, 0), (i * 94, 0), (i * 94, 846), width)  # Vertical lines
        pygame.draw.line(screen, (0, 0, 0), (0, i * 94), (846, i * 94), width)  # Horizontal lines


# Function to place numbers on the board
def draw_numbers(screen, board, selected_cord, sudoku_instance, sketched_values):
    font = pygame.font.Font(None, 60)  # Font for regular numbers
    small_font = pygame.font.Font(None, 30)  # Font for sketched numbers

    for row in range(9):
        for col in range(9):
            # Draw permanent or user-input numbers
            if sudoku_instance.board_original[row][col] != 0:  # Permanent numbers
                number = font.render(str(board[row][col]), True, (0, 0, 0))
                screen.blit(number, (col * 94 + 35, row * 94 + 25))
            elif board[row][col] != 0:  # User-input numbers
                number = font.render(str(board[row][col]), True, (0, 0, 0))
                screen.blit(number, (col * 94 + 35, row * 94 + 25))
            else:  # Sketched values
                for idx, sketch in enumerate(sketched_values[row][col]):
                    x_offset = col * 94 + 10 + (idx % 3) * 30  # Adjust for grid position
                    y_offset = row * 94 + 10 + (idx // 3) * 30
                    sketched_number = small_font.render(str(sketch), True, (100, 100, 100))
                    screen.blit(sketched_number, (x_offset, y_offset))

            # Highlight the selected cell
            if selected_cord is not None and [row, col] == selected_cord:
                rect = pygame.Rect(col * 94, row * 94, 94, 94)
                pygame.draw.rect(screen, (255, 0, 0), rect, 3)

def troubleshooter(sudoku = None,board=None,sketched_values=None,selected_cord=None):
    if board != None:
        print("board:")
        for row in board:
            print(row)

    if sketched_values != None:
        print(f"\nsketches:")
        for row in sketched_values:
            print (row)
    if selected_cord != None:
        print(f"Selcted cord: {selected_cord}",end = "=")
        print(board[selected_cord[0]][selected_cord[1]])
    if sudoku != None:
        print("\nSudoku Class:\nCorrect Answers")
        for row in sudoku.board_correct:
            print (row)
        print(f"Missing terms now")
        board_test = [[0 for i in range(9)] for i in range(9)]
        for i in range(9):
            row = sudoku.board_original[i]
            for j in range(9):
                correct_term = sudoku.board_correct[i][j]
                if board != None:
                    if correct_term != board[i][j] and board[i][j] != 0:
                        print(f"Position: {i},{j} is wrong, it shouldn't be {board[i][j]} and should be {correct_term}")
                        board_test[i][j] = sudoku.board_correct[i][j]
                if row[j] == 0:
                    board_test[i][j] = sudoku.board_correct[i][j]
        for row in board_test:
            print(row)

#from litzyriveroo
def find_next_vacant_box(current_cord, direction, sudoku_instance):
    row, col = current_cord
    if direction == "up":
        for r in range(row - 1, -1, -1):
            if sudoku_instance.board[r][col] == 0:
                return [r, col]
    elif direction == "down":
        for r in range(row + 1, 9):
            if sudoku_instance.board[r][col] == 0:
                return [r, col]
    elif direction == "left":
        for c in range(col - 1, -1, -1):
            if sudoku_instance.board[row][c] == 0:
                return [row, c]
    elif direction == "right":
        for c in range(col + 1, 9):
            if sudoku_instance.board[row][c] == 0:
                return [row, c]
    return None  # If no vacant cell is found in that direction

def user_input_valid(input_pos,sudoku_instance):
    #input_pos should be iteratable with index 0 being an x cord and index 1 being y cord
    #sudoku_instance will always be "sudoku" (not a string tho) because that's the var we called it
    if sudoku_instance.board_original[input_pos[0]][input_pos[1]] == 0:
        return True
    return False

def check_win(board, sudoku_instance):
    if board == sudoku_instance.board_correct:
        return True
    else:
        return False

def check_full(board):
    # Iterate through the board and check if there's any empty cell (value = 0)
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                return False  # Found an empty cell, return False
    return True  # All cells are filled


#class function to input users input into a singular cell
# class Cell:
#     def __init__ (self, value, row, col, screen):
#         self.value = value
#         self.row = row
#         self.col = col
#         self.screen = screen
#         self.sketched = 0
#         self.selected = False
#         self.width = 94
#         self.height = 94
#         self.x = col * self.width
#         self.y = row * self.height
#
#     def set_cell_value(self, value):
#         self.value = value
#
#     def set_sketched_value(self, value):
#         self.sketched = value
#
#     def draw(self):
#         rect = pygame.Rect(self.x, self.y, self.width, self.height)
#         pygame.draw.rect(self.screen, (255, 0, 0) if self.selected else (0, 0, 0), rect, 3 if self.selected else 1)
#         font = pygame.font.Font(None, 60)
#         if self.value != 0:
#             number = font.render(str(self.value), True, (0, 0, 0))
#             self.screen.blit(number, (self.x + 35, self.y + 25))  # Center numbers
#         elif self.sketched != 0:
#             sketched_number = font.render(str(self.sketched), True, (100, 100, 100))
#             self.screen.blit(sketched_number, (self.x + 10, self.y + 10))  # Top-left alignment for sketched numbers


def main():
    pygame.init()
    screen = pygame.display.set_mode((846, 900))
    pygame.display.set_caption("Sudoku")
    menu_bg = pygame.image.load('menu_bg2.png')
    menu_bg = pygame.transform.scale(menu_bg, (900, 900))

    font1 = pygame.font.SysFont('Arial', 61)
    easy_text = font1.render("Easy", True, (255, 255, 255), (250, 140, 0))
    medium_text = font1.render("Medium", True, (255,255,255), (250, 140, 0))
    hard_text = font1.render("Hard", True, (255,255,255), (250, 140, 0))
    easy_rect = easy_text.get_rect(center = (120, 535))
    medium_rect = medium_text.get_rect(center=(427, 535))
    hard_rect = hard_text.get_rect(center=(730, 535))


    screen.blit(menu_bg, (0, 0))
    screen.blit(easy_text, easy_rect)
    screen.blit(medium_text, medium_rect)
    screen.blit(hard_text, hard_rect)
    pygame.display.update()

    #((580, 379), (25, 25))
    #trouble_text = font1.render("Troubleshoot", True, (255, 255, 255), (250, 140, 0))
    trouble_rect = easy_rect.copy()
    trouble_rect = trouble_rect.move(460,-136)
    trouble_mode = False
    #screen.blit(trouble_text,trouble_rect)
    #pygame.display.update()

    # easy_rect.scale_by_ip(4, 2)
    # medium_rect.scale_by_ip(4, 2)
    # hard_rect.scale_by_ip(4, 2)


    font2 = pygame.font.SysFont('Arial', 41)
    bg_image = pygame.image.load('game_bg.png')
    bg_image = pygame.transform.scale(bg_image, (900, 940))
    reset_text = font2.render("Reset", True, (255, 255, 255), (250, 140, 0))
    restart_text_main = font2.render("Restart", True, (255, 255, 255), (250, 140, 0))
    exit_text = font2.render("Exit", True, (255, 255, 255), (250, 140, 0))
    reset_rect = reset_text.get_rect(center = (185, 872))
    restart_rect_main = restart_text_main.get_rect(center = (455, 872))
    exit_rect = exit_text.get_rect(center = (720, 872))


    bg_image_game_over = pygame.image.load('game_over5.png')
    bg_image_game_over = pygame.transform.scale(bg_image_game_over, (900, 900))
    bg_image_game_won = pygame.image.load('game_won5.png')
    bg_image_game_won = pygame.transform.scale(bg_image_game_won, (900, 900))

    restart_font = pygame.font.SysFont('Arial', 61)
    restart_text = restart_font.render("Restart", True, (255, 255, 255))  # "Restart" text
    restart_rect = restart_text.get_rect(center=(470, 520))  # Position the restart button

    difficulty_selected = False
    while not difficulty_selected:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if trouble_rect.collidepoint(pos):
                    if trouble_mode == False:
                        trouble_mode = True
                        print("Trouble shooting on")
                    elif trouble_mode == True:
                        trouble_mode = False
                        print("Trouble shooting off")
                if trouble_mode:
                    print(f"position:{pos}")
                if easy_rect.collidepoint(pos):
                    difficulty_selected = True
                    cells_removed = 30
                    sudoku = SudokuGenerator(9, cells_removed)
                elif medium_rect.collidepoint(pos):
                    difficulty_selected = True
                    cells_removed = 40
                    sudoku = SudokuGenerator(9, cells_removed)
                elif hard_rect.collidepoint(pos):
                    difficulty_selected = True
                    cells_removed = 50
                    sudoku = SudokuGenerator(9, cells_removed)


    screen.fill("light blue")
    board = sudoku.get_board()

    # Singular cell input
    #cells = [[Cell(board[row][col], row, col, screen) for col in range(9)] for row in range(9)]
    #selected = None
    selected_cord = None
    # sketched_values = [[0 for col in range(9)] for row in range(9)]
    sketched_values = [[[] for col in range(9)] for row in range(9)] #is it a list so the sketched values could be a nested list?
    game_over = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if not game_over:
                if event.type == pygame.KEYDOWN:
                    #from litzyriveroo
                    if event.key == pygame.K_UP:
                        if selected_cord is not None:
                            selected_cord = find_next_vacant_box(selected_cord, "up", sudoku)
                    elif event.key == pygame.K_DOWN:
                        if selected_cord is not None:
                            selected_cord = find_next_vacant_box(selected_cord, "down", sudoku)
                    elif event.key == pygame.K_LEFT:
                        if selected_cord is not None:
                            selected_cord = find_next_vacant_box(selected_cord, "left", sudoku)
                    elif event.key == pygame.K_RIGHT:
                        if selected_cord is not None:
                            selected_cord = find_next_vacant_box(selected_cord, "right", sudoku)


                    if selected_cord is not None:
                        if event.key in range(pygame.K_1, pygame.K_9 + 1):  # Check number input
                            num = event.key - pygame.K_0  # Convert key to number
                            if user_input_valid(selected_cord, sudoku):
                                # If the number is already in sketched_values, remove it
                                if num in sketched_values[selected_cord[0]][selected_cord[1]]:
                                    sketched_values[selected_cord[0]][selected_cord[1]].remove(num)
                                else:  # Otherwise, add the number to sketched_values
                                    sketched_values[selected_cord[0]][selected_cord[1]].append(num)
                        elif event.key in range(pygame.K_a, pygame.K_z + 1):  # Ignore letter keys
                            continue  # Skip processing for letter keys
                        elif event.key == pygame.K_RETURN:  # Finalize sketched value
                            if selected_cord is not None:
                                # Ensure sketched_values for the selected cell is not empty
                                if sketched_values[selected_cord[0]][selected_cord[1]]:
                                    # If not empty, retrieve the last sketched value
                                    value = sketched_values[selected_cord[0]][selected_cord[1]][-1]
                                    "I noticed an issue below which is the wrong function is called and the else state"
                                    if user_input_valid([selected_cord[0], selected_cord[1]], sudoku): #changed to be correct function
                                        # Set the value in the board and clear sketched values
                                        board[selected_cord[0]][selected_cord[1]] = value
                                        sketched_values[selected_cord[0]][selected_cord[1]] = []
                                    if trouble_mode:
                                        troubleshooter(sudoku,board,sketched_values,selected_cord)
                                    # else:
                                    #     board[selected_cord[0]][selected_cord[1]] = value
                                    #     sketched_values[selected_cord[0]][selected_cord[1]] = []
                        elif event.key == pygame.K_BACKSPACE:  # Remove the last sketched value
                            if selected_cord is not None:
                                if sketched_values[selected_cord[0]][selected_cord[1]]:
                                    # Remove the last sketched value
                                    sketched_values[selected_cord[0]][selected_cord[1]].pop()
                            # if enter key is pressed on a sketched value:
                            # that value becomes darker??? Not really clear in the guidelines
                            "the following code is correct and is just saved for when the enter key statement is added"
                            # board[selected_cord[0]][selected_cord[
                            #     1]] = event.key - pygame.K_0  # needed because draw_numbers uses board and not the class
                            # # this does not change the value of the spot inside the sudoku class, just the board variable made earlier


                if check_full(board):
                    if check_win(board, sudoku):  # Check if the player wins
                        screen.fill((255, 255, 255))
                        screen.blit(bg_image_game_won, (0, 0))
                        screen.blit(restart_text, restart_rect)
                        pygame.display.update()
                        game_over = True
                    else:
                        screen.fill((255, 255, 255))
                        screen.blit(bg_image_game_over, (0, 0))
                        screen.blit(restart_text, restart_rect)
                        pygame.display.update()
                        game_over = True

                if event.type == pygame.MOUSEBUTTONDOWN:  # clicked cell turns red
                    pos = pygame.mouse.get_pos()
                    cols = pos[0] // 94
                    rows = pos[1] // 94
                    selected_cord = [rows, cols]
                    # if trouble_mode:
                    #     print(f"position:{pos}, Board Cord: {selected_cord}")


                    if selected_cord is not None and 0 <= selected_cord[0] < 9 and 0 <= selected_cord[1] < 9:
                        #selected = cells[selected_cord[0]][selected_cord[1]]
                        selected_cord = [rows, cols]
                    else:
                        selected_cord = None
                        #selected = None  # or handle the case appropriately
                    if restart_rect_main.collidepoint(pos):
                        main()
                    elif reset_rect.collidepoint(pos):
                        board = copy.deepcopy(sudoku.board_original)
                        selected_cord = None
                        sketched_values = [[[] for col in range(9)] for row in range(9)]
                        draw_numbers(screen, board, selected_cord, sudoku, sketched_values)
                        #cells = [[Cell(board[row][col], row, col, screen) for col in range(9)] for row in range(9)]

                        game_over = False  # Reset game over state if any
                    elif exit_rect.collidepoint(pos):
                        exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if game_over and restart_rect.collidepoint(mouse_x, mouse_y):
                    main()


            if not game_over:
                # Clear the screen, draw grid, and numbers
                # screen.fill("light blue")
                screen.fill("light blue")
                draw_grid(screen)
                draw_numbers(screen, board, selected_cord, sudoku,sketched_values) #Can highlight the selected box. Also it needs the instance name to know which is user generated and which is OG
                screen.blit(reset_text, reset_rect)
                screen.blit(restart_text_main, restart_rect_main)
                screen.blit(exit_text, exit_rect)
                # for row in cells:
                #     for cell in row:
                #         if cell.selected: #iterating through is super inefficient so just the selected cell matters
                #             cell.draw()

                pygame.display.update()

if __name__ == "__main__":
    main()



# x = SudokuGenerator(9, 0)
# x.print_board()
