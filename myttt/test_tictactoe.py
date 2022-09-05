from ctypes import util
import math
from copy import deepcopy
import numpy as np

X = "X"
O = "O"

X_win = 0
O_win = 0
draw = 0

#helper
def get_diagonal(board):
    return [[board[0][0], board[1][1], board[2][2]],
            [board[0][2], board[1][1], board[2][0]]]

#helper
def get_columns(board):
    columns = []

    for i in range(3):
        columns.append([row[i] for row in board])

    return columns

#helper
def three_in_a_row(row):
    return True if row.count(row[0]) == 3 else False


def player(board):
    #    Returns player who has the next turn on a board.
    count_x=0
    count_o=0
    for i in board:
        for j in i:
            if(j=="X"):
                count_x=count_x+1
            if(j=="O"):
                count_o=count_o+1
    return O if count_x > count_o else X


def actions(board):
    # get all available empty cells for AI
    action=set()
    for i, row in enumerate(board):
        for j , vall in enumerate(row):
            if(vall==None):
                action.add((i,j))
    return action

def result(board, action):
    i,j=action
    if(board[i][j]!=None):
        raise Exception("Invalid Move ")
    next_move=player(board)
    deep_board=deepcopy(board)
    deep_board[i][j]=next_move
    return deep_board


def winner(board):
    # find the winner of the game
    rows=board+get_diagonal(board) +get_columns(board)
    for row in rows:
        current_palyer=row[0]
        if current_palyer is not None and three_in_a_row(row):
            return current_palyer
    return None

def terminal(board):
    # see if game is finished, does not return winner
    xx=winner(board)
    if(xx is  not None):
        return True
    if(all(all(j!=None for j in i) for i in board)):
        return True
    return False


def utility(board):
    xx=winner(board)
    if(xx==X):
        return 1
    elif(xx==O):
        return -1
    else:
        return 0 


def max_alpha_beta_pruning(board ,alpha,beta):
    if(terminal(board)== True):
        if utility(board) == 1:
            global X_win
            X_win += 1
        elif utility(board) == -1:
            global O_win
            O_win += 1
        else:
            global draw
            draw += 1
        return utility(board) , None
    vall=float("-inf")
    best=None
    for action in actions(board):
        min_val=min_alpha_beta_pruning(result(board ,action), alpha, beta)[0]
        if( min_val > vall):
            best=action
            vall=min_val
        alpha=max(alpha,vall)
        if (beta <= alpha):
            break
    return vall,best                                  

def min_alpha_beta_pruning(board ,alpha,beta):
    if(terminal(board)== True): 
        if utility(board) == 1:
            global X_win
            X_win += 1
        elif utility(board) == -1:
            global O_win
            O_win += 1
        else:
            global draw
            draw += 1
        return utility(board) , None
    vall=float("inf")
    best=None
    for action in actions(board):
        max_val=max_alpha_beta_pruning(result(board ,action), alpha, beta)[0]
        if( max_val < vall):
            best=action
            vall=max_val
        beta=min(beta,vall)
        if (beta <= alpha):
            break
    return vall,best


def minimax(board):
    if terminal(board):
        return None
    if(player(board)==X):
        return max_alpha_beta_pruning(board ,float("-inf") ,float("inf"))[1]
    elif(player(board) == O):
        return min_alpha_beta_pruning(board , float("-inf"), float("inf"))[1]
    else:
        raise Exception("Error in Caculating Optimal Move")

def show_AI_chances(board):
    AI_mark = player(board)
    chance = {}
    for action in actions(board):
        global O_win, X_win, draw
        O_win, X_win, draw = 0,0,0
        minimax(result(board, action))
        if terminal(result(board, action)):
            chance[action] = AI_mark+ "'s win move"
        if AI_mark == "X":
            try:
                chance[action] = round((X_win)/ (X_win+O_win+draw), 3)
            except ZeroDivisionError:
                print('Game Over')
        elif AI_mark == "O":
            try:
                chance[action] = round((O_win)/ (X_win+O_win+draw),3)
            except ZeroDivisionError:
                print('Game Over ===================================================')
                break
        print('action: ', action, 'x: ', X_win, 'o: ', O_win, 'draw: ', draw, 'chance: ', chance[action])
    return chance
