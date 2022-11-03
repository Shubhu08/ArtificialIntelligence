#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 16 23:21:57 2021

Author : Shubhashree Dash
"""
import numpy
import heapq

def elevation(array, x1,y1,x2,y2):
    height1=0 if(array[x1,y1] >= 0) else abs(array[x1,y1])
    height2=0 if(array[x2,y2] >= 0) else abs(array[x2,y2])
    return abs(height1-height2)

def chebyshev(current,goal):
    change_x = abs(current[0]-goal[0])
    change_y = abs(current[1]-goal[1])
    return 10*(change_x+change_y) - 4*min(change_x,change_y)

input_file = open("input.txt","r")
mode = input_file.readline().strip()
#print(mode)
width, height = map(int,input_file.readline().split())
#print(width, height)
start_X, start_Y = map(int, input_file.readline().split())
#print(start_X, start_Y)
max_rock_height = int(input_file.readline())
#print(max_rock_height)
N = int(input_file.readline())
#print(N)
goal_states = numpy.array([input_file.readline().split() for i in range(N)], dtype=int)
#print(goal_states)
map_array = numpy.array([input_file.readline().split() for i in range(height)], dtype=int)
#print(map_array)
map_array = map_array.transpose()
#mode = "BFS"
input_file.close()

output_file  = open("output.txt","w")
if(mode == "BFS"):
    for goal_state in goal_states:
        bool_path = False
        queue = [[(start_X,start_Y)]]
        seen = dict([])
        while queue:
            path = queue.pop(0)
            current_node = path[0]
            try:
                seen[current_node] = path[1]
            except:
                seen[current_node] = None
            if(current_node == tuple(goal_state)):
                bool_path = True
                #print(" ".join(str(x[0])+","+str(x[1]) for x in path))
                path_list = [current_node]
                node = current_node
                while seen[node] != None:
                    path_list.append(seen[node])
                    node = seen[node]
                path_list.reverse()
                output_file.write(" ".join(str(x[0])+","+str(x[1]) for x in path_list) + "\n")
                break
            else:
                for (x,y) in [ (i,j) for i in range(current_node[0]-1,current_node[0]+2) for j in range(current_node[1]-1, current_node[1]+2)]:
                    if(x<width and x>=0 and y<height and y>=0):
                        if( ((x,y) not in [node[0] for node in queue]) and ((x,y) not in seen.keys()) and (elevation(map_array,current_node[0],current_node[1],x,y) <= max_rock_height) ):
                            #print(queue)
                            queue.append([(x,y),current_node])

        if(not bool_path):
            #print("FAIL")
            output_file.write("FAIL" + "\n")

elif(mode == "UCS"):
    for goal_state in goal_states:
        bool_path = False
        queue_heap = []
        seen = dict([])
        heapq.heappush(queue_heap,[0,[(start_X,start_Y)]])
        #queue = [[[(start_X,start_Y)],0]]
        while queue_heap:
           #queue.sort(key = lambda sort_key : sort_key[-1])
           path = heapq.heappop(queue_heap)
           #print(path)
           #path = queue.pop(0)
           current_node = path[1][0]
           current_cost = path[0]
           try:
                seen[current_node] = path[1][1]
           except:
                seen[current_node] = None
           if(current_node == tuple(goal_state)):
               bool_path = True
               #print(" ".join(str(x[0])+","+str(x[1]) for x in path[1]))
               path_list = [current_node]
               node = current_node
               while seen[node] != None:
                   path_list.append(seen[node])
                   node = seen[node]
               path_list.reverse()
               output_file.write(" ".join(str(x[0])+","+str(x[1]) for x in path_list) + "\n")
               break;
           else:
                for (x,y) in [(current_node[0]+1,current_node[1]),(current_node[0]-1,current_node[1]),(current_node[0],current_node[1]+1),(current_node[0],current_node[1]-1)]:
                    if(x<width and x>=0 and y<height and y>=0):
                        if(((x,y) not in seen.keys()) and (elevation(map_array,current_node[0],current_node[1],x,y) <= max_rock_height)):
                            same_nodes = [node for node in queue_heap if node[1][0] == (x,y)]
                            if (not same_nodes):
                                heapq.heappush(queue_heap,[current_cost+10,[(x,y),current_node]])
                            else:
                                if (same_nodes[0][0] > current_cost+10):
                                    same_nodes[0] = [current_cost+10,[(x,y),current_node]]
                            #queue.append([path[0]+[(x,y)],current_cost+10])
                for (x,y) in [(current_node[0]-1,current_node[1]-1),(current_node[0]-1,current_node[1]+1),(current_node[0]+1,current_node[1]-1),(current_node[0]+1,current_node[1]+1)]:
                    if(x<width and x>=0 and y<height and y>=0):
                        if(((x,y) not in seen.keys()) and (elevation(map_array,current_node[0],current_node[1],x,y) <= max_rock_height)):
                            same_nodes = [node for node in queue_heap if node[1][0] == (x,y)]
                            if (not same_nodes):
                                heapq.heappush(queue_heap,[current_cost+14,[(x,y),current_node]])
                            else:
                                if (same_nodes[0][0] > current_cost+14):
                                    same_nodes[0] = [current_cost+14,[(x,y),current_node]]
                             #queue.append([path[0]+[(x,y)],current_cost+14])
        if(not bool_path):
            #print("FAIL")
            output_file.write("FAIL" + "\n")

elif(mode == "A*"):
    for goal_state in goal_states:
        bool_path = False
        queue_heap = []
        seen = dict([])
        heapq.heappush(queue_heap,[0,0,[(start_X,start_Y)]])
        #print(queue)
        while queue_heap:
           #print(queue_heap)
           path = heapq.heappop(queue_heap)
           #path = queue.pop(0)
           current_node = path[2][0]
           current_cost = path[1]
           try:
                seen[current_node] = [path[2][1],path[1]]
           except:
                seen[current_node] = [None,0]
           if(current_node == tuple(goal_state)):
               bool_path = True
               #print(" ".join(str(x[0])+","+str(x[1]) for x in path[2]))
               path_list = [current_node]
               node = current_node
               while seen[node][0] != None:
                   path_list.append(seen[node][0])
                   node = seen[node][0]
               path_list.reverse()
               output_file.write(" ".join(str(x[0])+","+str(x[1]) for x in path_list) + "\n")
               
               break
           else:
                for (x,y) in [(current_node[0]+1,current_node[1]),(current_node[0]-1,current_node[1]),(current_node[0],current_node[1]+1),(current_node[0],current_node[1]-1)]:
                    if(x<width and x>=0 and y<height and y>=0):
                        if(((x,y) not in seen.keys()) and (elevation(map_array,current_node[0],current_node[1],x,y) <= max_rock_height)):
                            cost = 10 + elevation(map_array,current_node[0],current_node[1],x,y) + (abs(map_array[x,y]) if map_array[x,y]>0 else 0)
                            same_nodes = [node for node in queue_heap if node[2][0] == (x,y)]
                            if (not same_nodes):
                                heapq.heappush(queue_heap, [int(chebyshev((x,y),goal_state))+current_cost+cost, current_cost+cost,[(x,y),current_node]])
                            elif (same_nodes[0][1] > current_cost + cost):
                                    queue_heap.remove(same_nodes[0]) 
                                    heapq.heappush(queue_heap, [int(chebyshev((x,y),goal_state))+current_cost+cost, current_cost+cost,[(x,y),current_node]])

                        if(((x,y) in seen.keys())):
                            if(seen[(x,y)][1] > current_cost + cost):
                                seen.pop((x,y))
                                heapq.heappush(queue_heap, [int(chebyshev((x,y),goal_state))+current_cost+cost, current_cost+cost,[(x,y),current_node]])                            
               
                for (x,y) in [(current_node[0]-1,current_node[1]-1),(current_node[0]-1,current_node[1]+1),(current_node[0]+1,current_node[1]-1),(current_node[0]+1,current_node[1]+1)]:
                    if(x<width and x>=0 and y<height and y>=0):
                        if(((x,y) not in seen.keys()) and (elevation(map_array,current_node[0],current_node[1],x,y) <= max_rock_height)):
                            cost = 14 + elevation(map_array,current_node[0],current_node[1],x,y) + (abs(map_array[x,y]) if map_array[x,y]>0 else 0)
                            same_nodes = [node for node in queue_heap if node[2][0] == (x,y)]
                            if (not same_nodes):
                                heapq.heappush(queue_heap, [int(chebyshev((x,y),goal_state))+current_cost+cost, current_cost+cost,[(x,y),current_node]])
                            elif (same_nodes[0][1] > current_cost + cost):
                                    queue_heap.remove(same_nodes[0]) 
                                    heapq.heappush(queue_heap, [int(chebyshev((x,y),goal_state))+current_cost+cost, current_cost+cost,[(x,y),current_node]])

                        if(((x,y) in seen.keys())):
                            if(seen[(x,y)][1] > current_cost + cost):
                                seen.pop((x,y))
                                heapq.heappush(queue_heap, [int(chebyshev((x,y),goal_state))+current_cost+cost, current_cost+cost,[(x,y),current_node]])                            
 
                            
        if(not bool_path):
            #print("FAIL")
            output_file.write("FAIL" + "\n")

output_file.close()
