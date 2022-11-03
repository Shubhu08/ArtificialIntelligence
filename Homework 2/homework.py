#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 16 13:41:38 2021

@author: shubhashreedash
"""
from copy import deepcopy
from math import inf
from itertools import product


class node:
    state = []
    parent_state = []
    #eval_value = 0
    move = []
    move_type = 'E'
    piece = ()
    player = ""
    player_type = 0

    def __init__(self, parent_state, state, piece, move, move_type, player, player_type):
        self.parent_state = deepcopy(parent_state)
        self.state = deepcopy(state)        
        self.move = deepcopy(move)
        self.move_type = deepcopy(move_type)
        self.piece = deepcopy(piece)
        self.player = deepcopy(player)
        self.player_type = deepcopy(player_type)
        self.eval_value = float(inf) if player_type == -1 else float(-inf)


class game_start:
    initial_state = []
    agent_player = ""
    
    def __init__(self,initial_state, agent_player):
        self.initial_state = deepcopy(initial_state)
        self.agent_player = deepcopy(agent_player)
    
def game_over(state_node):

    all_move = generate_all_states(state_node.state, state_node.player, state_node.player_type)

    if all_move == []:
        return True, []
    else:
        return False, all_move
        
def evaluation_funtion(state_node, game_agent, depth):
    
    over, move_states = game_over(state_node)   
    
    if over:
        return (500,[]) if state_node.player_type == -1 else (-500,[])
    
    value = state_node.eval_value
    value_change = state_node.eval_value
    #print("STATE MOVE : ",state_node.move)
    if depth == 0  :
        #print(state_node.state)
        value = 0
        no_of_pieces = 64 - sum([i.count(0) for i in state_node.state])
        if no_of_pieces >= 8:
            weight_array = [
            [5, 4, 3, 2, 2, 3, 4, 5],
            [4, 3, 2, 2, 2, 2, 3, 4],
            [3, 2, 2, 2, 2, 2, 2, 3],
            [3, 2, 1, 1, 1, 1, 2, 3],
            [3, 2, 1, 1, 1, 1, 2, 3],
            [3, 2, 2, 2, 2, 2, 2, 3],
            [4, 3, 2, 2, 2, 2, 3, 4],
            [5, 4, 3, 2, 2, 3, 4, 5]] 
    
        else:
            weight_array = [
            [2, 2, 2, 2, 2, 2, 2, 2],
            [2, 3, 3, 3, 3, 3, 3, 2],
            [2, 3, 4, 4, 4, 4, 3, 2],
            [2, 3, 4, 5, 5, 4, 3, 2],
            [2, 3, 4, 5, 5, 4, 3, 2],
            [2, 3, 4, 4, 4, 4, 3, 2],
            [2, 3, 3, 3, 3, 3, 3, 2],
            [2, 2, 2, 2, 2, 2, 2, 2]] 
    
        weighted_node = [[state_node.state[i][j]*weight_array[i][j] for j in range(8)] for i in range(8)]
        final_position = state_node.move[-1] if(isinstance(state_node.move,list)) else state_node.move #and isinstance(state_node.move[1],tuple)) 
        distance = 0
        try:
            if(state_node.state[final_position[0]][final_position[1]] > 0):
                pieces = select_piece(state_node.state, "BLACK", -1)
                for piece in pieces:
                    distance = distance + max(abs(final_position[0]-piece[0]),abs(final_position[1]-piece[1]))
            else:
                pieces = select_piece(state_node.state, "BLACK", 1)
                for piece in pieces:
                    distance = distance + max(abs(final_position[0]-piece[0]),abs(final_position[1]-piece[1]))         
                distance = -distance
        
        except:
            distance = 0
            
        value_change = sum([sum(i) for i in state_node.state]) - sum([sum(i) for i in game_agent.state])
        
        value = sum([sum(i) for i in weighted_node]) - (distance/no_of_pieces) + value_change
        #print("VALUE : ",value,state_node.player,state_node.piece)
    #return value_change, move_states
    return value, move_states

def split_move(element):
    if(isinstance(element,tuple) and isinstance(element[1],tuple)):
        return [element[0]] + split_move(element[1])
    else:
        return [element]
    
def generate_moves(board, player, piece, consecutive_jump = False):
    moves = dict({'J' : [], 'E' : []})
    #Jump moves
    if(player == "BLACK"):
        if(abs(board[piece[0]][piece[1]]) == 1):
            move1 = (piece[0] + 2, piece[1] + 2) if (piece[0] + 2 < 8) and (piece[1] + 2 < 8) and (piece[0] + 1 < 8) and (piece[1] + 1 < 8) and (board[piece[0]+1][piece[1]+1]*board[piece[0]][piece[1]] < 0 and board[piece[0]+2][piece[1]+2] == 0) else None
            move2 = (piece[0] + 2, piece[1] - 2) if (piece[0] + 2 < 8) and (piece[1] - 2 >=0) and (piece[0] + 1 < 8) and (piece[1] - 1 >=0) and (board[piece[0]+1][piece[1]-1]*board[piece[0]][piece[1]] < 0 and board[piece[0]+2][piece[1]-2] == 0) else None
            comb_move1 = [move1]
            comb_move2 = [move2]
            if move1 != None : 
                comb_move1 = list(product([move1], generate_moves(create_state(board,piece,move1), player, move1, True)['J']))
                if(comb_move1 == []): comb_move1 = [move1]
            if move2 != None :
                comb_move2 = list(product([move2], generate_moves(create_state(board,piece,move2), player, move2, True)['J']))
                if(comb_move2 == []): comb_move2 = [move2]
            moves['J'] = moves['J'] + comb_move1 + comb_move2
            
        if(abs(board[piece[0]][piece[1]]) == 3):
            move1 = (piece[0] + 2, piece[1] + 2) if (piece[0] + 2 < 8) and (piece[1] + 2 < 8) and (piece[0] + 1 < 8) and (piece[1] + 1 < 8) and (board[piece[0]+1][piece[1]+1]*board[piece[0]][piece[1]] < 0 and board[piece[0]+2][piece[1]+2] == 0) else None
            move2 = (piece[0] + 2, piece[1] - 2) if (piece[0] + 2 < 8) and (piece[1] - 2 >=0) and (piece[0] + 1 < 8) and (piece[1] - 1 >=0) and (board[piece[0]+1][piece[1]-1]*board[piece[0]][piece[1]] < 0 and board[piece[0]+2][piece[1]-2] == 0) else None
            move3 = (piece[0] - 2, piece[1] + 2) if (piece[0] - 2 >=0) and (piece[1] + 2 < 8) and (piece[0] - 1 >=0) and (piece[1] + 1 < 8) and (board[piece[0]-1][piece[1]+1]*board[piece[0]][piece[1]] < 0 and board[piece[0]-2][piece[1]+2] == 0) else None
            move4 = (piece[0] - 2, piece[1] - 2) if (piece[0] - 2 >=0) and (piece[1] - 2 >=0) and (piece[0] - 1 >=0) and (piece[1] - 1 >=0) and (board[piece[0]-1][piece[1]-1]*board[piece[0]][piece[1]] < 0 and board[piece[0]-2][piece[1]-2] == 0) else None
            comb_move1 = [move1]
            comb_move2 = [move2]
            comb_move3 = [move3]
            comb_move4 = [move4]
            
            if move1 != None : 
                comb_move1 = list(product([move1], generate_moves(create_state(board,piece,move1), player, move1, True)['J']))
                if(comb_move1 == []): comb_move1 = [move1]
            if move2 != None :
                comb_move2 = list(product([move2], generate_moves(create_state(board,piece,move2), player, move2, True)['J']))
                if(comb_move2 == []): comb_move2 = [move2]
            if move3 != None : 
                comb_move3 = list(product([move3], generate_moves(create_state(board,piece,move3), player, move3, True)['J']))
                if(comb_move3 == []): comb_move3 = [move3]
            if move4 != None :
                comb_move4 = list(product([move4], generate_moves(create_state(board,piece,move4), player, move4, True)['J']))
                if(comb_move4 == []): comb_move4 = [move4]

            moves['J'] = moves['J'] + comb_move1 + comb_move2 + comb_move3 + comb_move4

    if(player == "WHITE"):
        if(abs(board[piece[0]][piece[1]]) == 1):   
            move1 = (piece[0] - 2, piece[1] + 2) if (piece[0] - 2 >=0) and (piece[1] + 2 < 8) and (piece[0] - 1 >=0) and (piece[1] + 1 < 8) and (board[piece[0]-1][piece[1]+1]*board[piece[0]][piece[1]] < 0 and board[piece[0]-2][piece[1]+2] == 0) else None
            move2 = (piece[0] - 2, piece[1] - 2) if (piece[0] - 2 >=0) and (piece[1] - 2 >=0) and (piece[0] - 1 >=0) and (piece[1] - 1 >=0) and (board[piece[0]-1][piece[1]-1]*board[piece[0]][piece[1]] < 0 and board[piece[0]-2][piece[1]-2] == 0) else None
            comb_move1 = [move1]
            comb_move2 = [move2]
            if move1 != None : 
                comb_move1 = list(product([move1], generate_moves(create_state(board,piece,move1), player, move1, True)['J']))
                if(comb_move1 == []): comb_move1 = [move1]
            if move2 != None :
                comb_move2 = list(product([move2], generate_moves(create_state(board,piece,move2), player, move2, True)['J']))
                if(comb_move2 == []): comb_move2 = [move2]
            moves['J'] = moves['J'] + comb_move1 + comb_move2

            
        if(abs(board[piece[0]][piece[1]]) == 3):
            move1 = (piece[0] + 2, piece[1] + 2) if (piece[0] + 2 < 8) and (piece[1] + 2 < 8) and (piece[0] + 1 < 8) and (piece[1] + 1 < 8) and (board[piece[0]+1][piece[1]+1]*board[piece[0]][piece[1]] < 0 and board[piece[0]+2][piece[1]+2] == 0) else None
            move2 = (piece[0] + 2, piece[1] - 2) if (piece[0] + 2 < 8) and (piece[1] - 2 >=0) and (piece[0] + 1 < 8) and (piece[1] - 1 >=0) and (board[piece[0]+1][piece[1]-1]*board[piece[0]][piece[1]] < 0 and board[piece[0]+2][piece[1]-2] == 0) else None
            move3 = (piece[0] - 2, piece[1] + 2) if (piece[0] - 2 >=0) and (piece[1] + 2 < 8) and (piece[0] - 1 >=0) and (piece[1] + 1 < 8) and (board[piece[0]-1][piece[1]+1]*board[piece[0]][piece[1]] < 0 and board[piece[0]-2][piece[1]+2] == 0) else None
            move4 = (piece[0] - 2, piece[1] - 2) if (piece[0] - 2 >=0) and (piece[1] - 2 >=0) and (piece[0] - 1 >=0) and (piece[1] - 1 >=0) and (board[piece[0]-1][piece[1]-1]*board[piece[0]][piece[1]] < 0 and board[piece[0]-2][piece[1]-2] == 0) else None
            comb_move1 = [move1]
            comb_move2 = [move2]
            comb_move3 = [move3]
            comb_move4 = [move4]
            
            if move1 != None : 
                comb_move1 = list(product([move1], generate_moves(create_state(board,piece,move1), player, move1, True)['J']))
                if(comb_move1 == []): comb_move1 = [move1]
            if move2 != None :
                comb_move2 = list(product([move2], generate_moves(create_state(board,piece,move2), player, move2, True)['J']))
                if(comb_move2 == []): comb_move2 = [move2]
            if move3 != None : 
                comb_move3 = list(product([move3], generate_moves(create_state(board,piece,move3), player, move3, True)['J']))
                if(comb_move3 == []): comb_move3 = [move3]
            if move4 != None :
                comb_move4 = list(product([move4], generate_moves(create_state(board,piece,move4), player, move4, True)['J']))
                if(comb_move4 == []): comb_move4 = [move4]
            moves['J'] = moves['J'] + comb_move1 + comb_move2 + comb_move3 + comb_move4

    if list(filter(None, moves['J'])) != [] : consecutive_jump = True

    #Adjacent moves
    if(not consecutive_jump):
        if(player == "BLACK"):
            if(abs(board[piece[0]][piece[1]]) == 1):
                move1 = (piece[0] + 1, piece[1] + 1) if (piece[0] + 1 < 8) and (piece[1] + 1 < 8) and (board[piece[0]+1][piece[1]+1] == 0) else None
                move2 = (piece[0] + 1, piece[1] - 1) if (piece[0] + 1 < 8) and (piece[1] - 1 >=0) and (board[piece[0]+1][piece[1]-1] == 0) else None
                moves['E'] = moves['E'] + [move1, move2]
                
            if(abs(board[piece[0]][piece[1]]) == 3):
                move1 = (piece[0] + 1, piece[1] + 1) if (piece[0] + 1 < 8) and (piece[1] + 1 < 8) and (board[piece[0]+1][piece[1]+1] == 0) else None
                move2 = (piece[0] + 1, piece[1] - 1) if (piece[0] + 1 < 8) and (piece[1] - 1 >=0) and (board[piece[0]+1][piece[1]-1] == 0) else None
                move3 = (piece[0] - 1, piece[1] + 1) if (piece[0] - 1 >=0) and (piece[1] + 1 < 8) and (board[piece[0]-1][piece[1]+1] == 0) else None
                move4 = (piece[0] - 1, piece[1] - 1) if (piece[0] - 1 >=0) and (piece[1] - 1 >=0) and (board[piece[0]-1][piece[1]-1] == 0) else None
                moves['E'] = moves['E'] + [move1, move2, move3, move4]
    
        if(player == "WHITE"):
            if(abs(board[piece[0]][piece[1]]) == 1):
                move1 = (piece[0] - 1, piece[1] + 1) if (piece[0] - 1 >= 0) and (piece[1] + 1 < 8) and (board[piece[0]-1][piece[1]+1] == 0) else None
                move2 = (piece[0] - 1, piece[1] - 1) if (piece[0] - 1 >= 0) and (piece[1] - 1 >=0) and (board[piece[0]-1][piece[1]-1] == 0) else None
                moves['E'] = moves['E'] + [move1, move2]
                
            if(abs(board[piece[0]][piece[1]]) == 3):
                move1 = (piece[0] + 1, piece[1] + 1) if (piece[0] + 1 < 8) and (piece[1] + 1 < 8) and (board[piece[0]+1][piece[1]+1] == 0) else None
                move2 = (piece[0] + 1, piece[1] - 1) if (piece[0] + 1 < 8) and (piece[1] - 1 >=0) and (board[piece[0]+1][piece[1]-1] == 0) else None
                move3 = (piece[0] - 1, piece[1] + 1) if (piece[0] - 1 >=0) and (piece[1] + 1 < 8) and (board[piece[0]-1][piece[1]+1] == 0) else None
                move4 = (piece[0] - 1, piece[1] - 1) if (piece[0] - 1 >=0) and (piece[1] - 1 >=0) and (board[piece[0]-1][piece[1]-1] == 0) else None
                moves['E'] = moves['E'] + [move1, move2, move3, move4]

        
    final_moves = dict({'J' : list(filter(None,moves['J'])), 'E' : list(filter(None,moves['E']))})
#    print("Moves : ",moves)
#    print("State : ",board)
    return final_moves

def select_piece(board, player, player_type): # player is white or black to get order, player_type 1 = max, -1 = min
    pieces = []
    if (player == "BLACK"):
        for i in range(7,-1,-1):
            new_pieces = [(i,j) for j,val in enumerate(board[i]) if val == player_type*1 or val == player_type*3] 
            if new_pieces != []:
                pieces = pieces + new_pieces
    else:
        for i in range(8):
            new_pieces = [(i,j) for j,val in enumerate(board[i]) if val == player_type*1 or val == player_type*3] 
            if new_pieces != []:
                pieces = pieces + new_pieces
    return pieces

def read_board():
    input_file = open("input.txt", 'r')
    mode = input_file.readline().strip()
    player = input_file.readline().strip()
    time = float(input_file.readline().strip())
    score = []
    if (player == "BLACK"):
        score = dict({'b' : 1,'B' : 3 ,'w' : -1,'W' : -3 ,'.' : 0})
    else:
        score = dict({'b' : -1,'B' : -3 ,'w' : 1,'W' : 3 ,'.' : 0})
        
    input_board = [[score[i] for i in list(input_file.readline().strip())] for _ in range(8)]
    return mode, player, time , input_board

def create_state(board, piece, move):
    new_board = deepcopy(board)
    new_board[move[0]][move[1]] = board[piece[0]][piece[1]]
    new_board[piece[0]][piece[1]] = 0
    change_x = (piece[0] - move[0])//2 if (piece[0] - move[0]) != -1 else 0
    change_y = (piece[1] - move[1])//2 if (piece[1] - move[1]) != -1 else 0
    new_board[piece[0]-change_x][piece[1]-change_y] = 0
    return new_board

def generate_all_states(board, player, player_type):
    states = {'J' : [], 'E' : []}
    order_pieces = select_piece(board, player, player_type)
    
    for order_piece in order_pieces:
        
        moves = generate_moves(board, player, order_piece)
        update_moves = {'J' : [], 'E' : []}
        for jump_moves in moves['J']:
            update_moves['J'] = update_moves['J'] + [split_move(jump_moves)]
            
        update_moves['E'] = moves['E']

        if(update_moves['J'] != []):
            for move in update_moves['J']:
                game_board = deepcopy(board)
                piece = deepcopy(order_piece)
                for single_move in move :

                    new_board = create_state(game_board, piece, single_move)
                    game_board = new_board
                    piece = single_move
                states['J'] = states['J'] + [node(board, new_board, order_piece,move,'J', player, player_type)]

        else:
            for move in update_moves['E']:
                new_board = create_state(board, order_piece, move)

                states['E'] = states['E'] + [node(board, new_board,order_piece,move,'E', player, player_type)]
    
    if states['J'] != []:
        return states['J']
    return states['E']

def print_output(state_node):
    start_position = deepcopy(state_node.piece)
    row_position = [8,7,6,5,4,3,2,1]
    col_position = ['a','b','c','d','e','f','g','h']
    output_file = open("output.txt", "w")
    if(isinstance(state_node.move,tuple)):
        end_position = state_node.move
        output_file.write(str(state_node.move_type)+" "+str(col_position[start_position[1]])+str(row_position[start_position[0]])+" "+str(col_position[end_position[1]])+str(row_position[end_position[0]])+"\n")
        print(str(state_node.move_type)+" "+str(col_position[start_position[1]])+str(row_position[start_position[0]])+" "+str(col_position[end_position[1]])+str(row_position[end_position[0]]))
    else :
       for end_position in state_node.move:
           output_file.write(str(state_node.move_type)+" "+str(col_position[start_position[1]])+str(row_position[start_position[0]])+" "+str(col_position[end_position[1]])+str(row_position[end_position[0]])+"\n")
           print(str(state_node.move_type)+" "+str(col_position[start_position[1]])+str(row_position[start_position[0]])+" "+str(col_position[end_position[1]])+str(row_position[end_position[0]]))
           start_position = end_position
        


def min_value(state_node, alpha, beta, game_agent,depth):
    
    new_player = "BLACK" if state_node.player == "WHITE" else "WHITE"
    next_move_node = deepcopy(state_node)
    next_move_node.player = new_player
    next_move_node.player_type = -1
    
    
    value, move_nodes = evaluation_funtion(next_move_node, game_agent,depth)

    if move_nodes != [] and depth > 0:
        min_valued_state = move_nodes[0]
        min_valued_state.eval_value = float(inf)
        
        for move_node in move_nodes:
            
            
            max_value_result = max_value(move_node, alpha, beta, game_agent,depth-1)

            if min_valued_state.eval_value > max_value_result.eval_value:
                min_valued_state = move_node
                min_valued_state.eval_value = max_value_result.eval_value
                
 
#            if min_valued_state.eval_value <= alpha :      
#                return min_valued_state 
            beta = min(beta, min_valued_state.eval_value)
            
        
    else:
        state_node.eval_value = value
        return state_node
    
    return min_valued_state
        
def max_value(state_node, alpha, beta, game_agent, depth):

    new_player = "BLACK" if state_node.player == "WHITE" else "WHITE"
    next_move_node = deepcopy(state_node)
    next_move_node.player = new_player
    next_move_node.player_type = 1
    
    value, move_nodes = evaluation_funtion(next_move_node, game_agent, depth)

    if move_nodes != [] and depth > 0:
        max_valued_state = move_nodes[0]
        max_valued_state.eval_value = float(-inf)
        
        for move_node in move_nodes :
            min_value_result = min_value(move_node, alpha, beta, game_agent,depth-1)
            if max_valued_state.eval_value < min_value_result.eval_value:
                max_valued_state = move_node
                max_valued_state.eval_value = min_value_result.eval_value

#            if max_valued_state.eval_value >= beta :
#                return max_valued_state
            
            alpha = max(alpha, max_valued_state.eval_value)
        
    else:
        state_node.eval_value = value
        return state_node
    
    return max_valued_state


def alpha_beta_search(start,depth):
    new_player = "BLACK" if start.player == "WHITE" else "WHITE"
    next_move_node = deepcopy(start)
    next_move_node.player = new_player
    next_move_node.player_type = -1

    state = max_value(next_move_node,float(-inf),float(inf),start,depth)
    return state

       
mode, player, time , input_board = read_board()
game_agent = node([], input_board, (), (), "", player, 1)

if mode == "SINGLE":

    for state in generate_all_states(input_board, player, 1): 
        print_output(state)
        break

elif mode =="GAME":
    if(time<0.1):
        for state in generate_all_states(input_board, player, 1): 
            print_output(state)
            break
    elif(time<2):
        final_state = alpha_beta_search(game_agent,3)
        print_output(final_state)
    else:
        final_state = alpha_beta_search(game_agent,5)
        print_output(final_state)
    
#    print("Final State : ",final_state.piece,final_state.move)