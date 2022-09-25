import math
from copy import deepcopy
import numpy as np


X = "X"
O = "O"
chance = {}

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


def max_alpha_beta_pruning(board ,alpha,beta,layer):
    if(terminal(board)== True):
        return utility(board) , None

    global chance

    vall=float("-inf")
    best=None
    for action in actions(board):
        min_val=min_alpha_beta_pruning(result(board ,action), alpha, beta,layer+1)[0]
        if layer == 0:
            chance[action] = min_val

        if( min_val > vall): 
            best=action
            vall=min_val
        alpha=max(alpha,vall)
        if (beta <= alpha):
            break
    return vall,best                               

def min_alpha_beta_pruning(board ,alpha,beta, layer):
    if(terminal(board)== True): 
        return utility(board) , None

    global chance

    vall=float("inf")
    best=None
    for action in actions(board):
        max_val=max_alpha_beta_pruning(result(board ,action), alpha, beta,layer+1)[0]
        if layer == 0:
            chance[action] = max_val
        
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
        return max_alpha_beta_pruning(board ,float("-inf") ,float("inf"), 0)[1]
    elif(player(board) == O):
        return min_alpha_beta_pruning(board , float("-inf"), float("inf"), 0)[1]
    else:
        raise Exception("Error in Caculating Optimal Move")

def show_AI_chances(board):
    global chance
    for row in range(3):
        for col in range(3):
            if board[row][col] != None and (row,col) in chance:
                chance.pop((row,col))
    for c in chance:
        print(c, chance[c])
    return chance