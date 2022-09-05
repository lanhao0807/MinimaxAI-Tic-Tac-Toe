import pygame
import sys
import time

import test_tictactoe as ttt

pygame.init()
WIDTH = 600
HEIGHT = WIDTH
LINE_WIDTH = 15
BOARD_ROWS = 3
BOARD_COLS = 3
CIRCLE_RADIUS = 60
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = 55

RED = (255, 0, 0)
BLACK = (0, 0, 0)
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)
WHITE = (255, 255, 255)

user = None
ai_turn = False
board = [   [None, None, None],
            [None, None, None],
            [None, None, None] ]


screen = pygame.display.set_mode((WIDTH,HEIGHT))
mediumFont = pygame.font.Font(None, 28)
welcomePage = pygame.transform.scale(pygame.image.load('storyboard6.png').convert(), (WIDTH, HEIGHT))

# pygame drawings====================================================================================================
def draw_lines():
	# draw board cells
	# horizontal
	pygame.draw.line(screen, LINE_COLOR, (0, 200), (600, 200), LINE_WIDTH)
	pygame.draw.line(screen, LINE_COLOR, (0, 400), (600, 400), LINE_WIDTH)
	# vertical
	pygame.draw.line(screen, LINE_COLOR, (200, 0), (200, 600), LINE_WIDTH)
	pygame.draw.line(screen, LINE_COLOR, (400, 0), (400, 600), LINE_WIDTH)

def draw_figures():
	# draw circle and cross marks
	for row in range(BOARD_ROWS):
		for col in range(BOARD_COLS):
			if board[row][col] == 'O':
				pygame.draw.circle(screen, CIRCLE_COLOR, 
					(int( col*200+100 ), int( row*200+100  ) ), CIRCLE_RADIUS, CIRCLE_WIDTH)
			if board[row][col] == 'X':
				pygame.draw.line(screen, CROSS_COLOR, (col* 200+SPACE, row*200+200-SPACE), (col*200+200-SPACE, row*200+SPACE), CROSS_WIDTH)
				pygame.draw.line(screen, CROSS_COLOR, (col* 200+SPACE, row*200+SPACE), (col*200+200-SPACE, row*200+200-SPACE), CROSS_WIDTH)

def check_win(player):
	# vertical win check
	for col in range(BOARD_COLS):
		if board[0][col] == player and board[1][col] == player and board[2][col]==player:
			draw_vertical_winning_line(col,player)
			return True

	# horizontal win check
	for row in range(BOARD_ROWS):
		if board[row][0] == player and board[row][1] == player and board[row][2]==player:
			draw_horizontal_winning_line(row,player)
			return True

	# diagonal win check
	if board[2][0] == player and board[1][1] == player and board[0][2]==player:
			draw_asc_diagonal(player)
			return True
	if board[0][0] == player and board[1][1] == player and board[2][2]==player:
			draw_desc_diagonal(player)
			return True
	return False

def draw_vertical_winning_line(col, player):
	posX = col*200+100
	if player == 'O':
		color = CIRCLE_COLOR
	elif player == 'X':
		color = CROSS_COLOR
	pygame.draw.line(screen, color, (posX, 15), (posX, HEIGHT-15), 15)

def draw_horizontal_winning_line(row, player):
	posY = row*200+100
	if player == 'O':
		color = CIRCLE_COLOR
	elif player == 'X':
		color = CROSS_COLOR
	pygame.draw.line(screen, color, (15, posY), (WIDTH-15, posY), 15)

def draw_asc_diagonal(player):
	if player == 'O':
		color = CIRCLE_COLOR
	elif player == 'X':
		color = CROSS_COLOR

	pygame.draw.line(screen, color, (15, HEIGHT-15), (WIDTH-15, 15), 15)

def draw_desc_diagonal(player):
	if player == 'O':
		color = CIRCLE_COLOR
	elif player == 'X':
		color = CROSS_COLOR

	pygame.draw.line(screen, color, (15,15), (WIDTH-15, HEIGHT-15), 15)
# pygame drawings====================================================================================================

def show_numbers_in_board(chances):
    for chance in chances:
        i, j =  chance
        x_pos = j*200 + 100
        y_pos = i*200 + 100
        score = mediumFont.render(str(chances[chance]), True, WHITE)
        scoreRect = score.get_rect()    
        scoreRect.center = (x_pos, y_pos)
        # show numbers and erase numbers
        screen.blit(score, scoreRect)
        pygame.display.flip()

    pygame.time.wait(1000)
    for chance in chances:
        i, j =  chance
        x_pos = j*200 + 100
        y_pos = i*200 + 100
        score1 = mediumFont.render(str(chances[chance]), True, WHITE)
        # eraser that covers the numbers
        era = score1.get_rect() 
        era.center = (x_pos, y_pos)
        pygame.draw.rect(screen, BG_COLOR, era, 0)


def start():
    screen.fill(BG_COLOR)
    draw_lines()
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            board[row][col] = None

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    if user is None:
        screen.blit(welcomePage, (0,0))
            # Draw title
        title = mediumFont.render("Play Tic-Tac-Toe", True, BLACK)
        titleRect = title.get_rect()
        titleRect.center = ((WIDTH / 2), 50)
        screen.blit(title, titleRect)
            # Draw chose player buttons
        playXButton = pygame.Rect((WIDTH/2)-titleRect.width/2 , (HEIGHT / 3), WIDTH / 4, 40)
        playX = mediumFont.render("1st: Press X", True, BLACK)
        playXRect = playX.get_rect()
        playXRect.center = playXButton.center
        pygame.draw.rect(screen, BG_COLOR, playXButton)
        screen.blit(playX, playXRect)

        playOButton = pygame.Rect((WIDTH/2)-titleRect.width/2, (HEIGHT / 3) +100, WIDTH / 4, 40)
        playO = mediumFont.render("2nd: Press O", True, BLACK)
        playORect = playO.get_rect()
        playORect.center = playOButton.center
        pygame.draw.rect(screen, BG_COLOR, playOButton) 
        screen.blit(playO, playORect)
            # hit X play as x and hit O play as o
        key = pygame.key.get_pressed()
        if key[pygame.K_x]:
            user = ttt.X
            screen.fill(BG_COLOR)
            draw_lines()
        elif key[pygame.K_o]:
            user = ttt.O
            screen.fill(BG_COLOR)
            draw_lines()
    else:
        game_over = ttt.terminal(board)
        player = ttt.player(board)

        # Check for AI move
        if user != player and not game_over:
            if ai_turn:
                chance_map = ttt.show_AI_chances(board)
                show_numbers_in_board(chance_map)               
                board = ttt.result(board, ttt.minimax(board))
                draw_figures()
                check_win(player)
                ai_turn = False
                print("AI move:\n", board)
            else:
                ai_turn = True

        # Check for a user move
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1 and user == player and not game_over:
            # show_minimax_score()
            mouseX, mouseY = pygame.mouse.get_pos()
            clicked_row = int(mouseY // 200)
            clicked_col = int(mouseX // 200)
            if (board[clicked_row][clicked_col] == None):
                board = ttt.result(board, (clicked_row, clicked_col))
                draw_figures()
                check_win(player)
                print("player move: \n", board)

        if game_over: 
            # restart by press key "X" or "O"
            againButton = pygame.Rect(WIDTH /3 - 45, HEIGHT - 45, WIDTH / 2, 40)
            again = mediumFont.render("Press x/o to replay as", True, BLACK)
            againRect = again.get_rect()
            againRect.center = againButton.center
            pygame.draw.rect(screen, WHITE, againButton)
            screen.blit(again, againRect)
            key = pygame.key.get_pressed()
            if key[pygame.K_x]:
                user = ttt.X
                ai_turn = False
                start()
            elif key[pygame.K_o]:
                user = ttt.O
                ai_turn = True
                start()

    pygame.display.flip()