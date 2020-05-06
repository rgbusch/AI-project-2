import copy 
from cmath import sqrt
import math as m

import random

class Node:
    def __init__(self, state=None,child = [],action = None,move = None,depth =None, reward = 0):
        self.state = state
        self.child = child
        self.move = move
        self.action = action
        self.depth = depth
        self.reward = reward

def weight_update(reward_score,learning_rate,lamda,weight):

    print("=============================")
    print("\n")
    print("\n")
    print("\n")
    print("\n")
    print("\n")
    print("=============================")

    sum_weights = sum(weight)
    return_weight = []

    total_sum = 0
    for y in range(len(reward_score)-1):
        second_part = 0
        for z in range(y,len(reward_score)-1):
            second_part += m.pow(lamda,(z-y)) * (reward_score[y+1] - reward_score[y])
        #derivate of tanh(w * f(s)) = f(s) * sech^2(w * f(s))
        #as rewards are already presented after calculating tanh(w * f(s))
        #by applying arctanh and dividing by the sum of weigths will help us obtain f(s) at that point
        fs = m.atanh(reward_score[y])/sum_weights
        #sech can be represented by 1/cosh which cosh is included in the maths library
        sech_square = m.pow(1/m.cosh(reward_score[y]),2)
        combined = fs * sech_square * second_part
        total_sum += combined
    total_sum = total_sum * learning_rate

    for w in weight:
        return_weight.append(w + total_sum)

    f = open("your_team_name/weights.txt","w+")
    temp_str = ""
    for w in return_weight:
        if w != return_weight[-1]:
            temp_str += (str(w) + ",")
        else:
            temp_str += (str(w))
    f.write(temp_str)
    f.close()




def branch_approximation(current_node,colour):
    possible_moves = 0
    if (current_node.state[colour]):
        for stack_num in range(len(current_node.state[colour])):
            maximum_moves = current_node.state[colour][stack_num][0]*current_node.state[colour][stack_num][0]*4 + 1
            move_range = current_node.state[colour][stack_num][0]
            for x in range(-(move_range),move_range+1):
                if (in_bounds(current_node.state,stack_num,[abs(x),0,x],colour)) == False:
                    maximum_moves -= 1*current_node.state[colour][stack_num][0]
                if (in_bounds(current_node.state,stack_num,[abs(x),x,0],colour)) == False:
                    maximum_moves -= 1*current_node.state[colour][stack_num][0]
            possible_moves += maximum_moves
    else: # prevents getting stuck in for loop in update if no stacks
        return 20
    return possible_moves



def evaluation(current_node,colour,weights):
    """
    temp_dict = {}
    temp_node = copy.deepcopy(current_node)
    for x in range(len(weights)):
        white_count = 0
        black_count = 0
        for w_tokens in temp_node.state["white"]:
            if w_tokens[0] == x + 1:
                white_count += 1
                temp_node.state["white"].remove(w_tokens)
        for b_tokens in temp_node.state["black"]:
            if b_tokens[0] == x + 1:
                black_count += 1
                temp_node.state["black"].remove(b_tokens)
        if colour == "white":
            temp_dict[x] = weights[x] * (white_count - black_count)
        else:
            temp_dict[x] = weights[x] * (black_count - white_count)
    temp_sum = 0
    
    for keys in temp_dict:
        temp_sum += temp_dict[keys]
    
    """
    temp_sum = 0
    w = [0,0,0,0,0,0,0,0,0,0,0,0]
    b = [0,0,0,0,0,0,0,0,0,0,0,0]
    for x in current_node.state['white'] :
        w[x[0]-1] += 1
    for x in current_node.state['black'] :
        b[x[0]-1] += 1
    
    if colour == 'white' :
        other = 'black'
    else :
        other = 'white'
    
    for x in range(len(weights)) :
        temp_sum += weights[x] * (w[x] - b[x])
    if colour == 'black' :
        temp_sum = -1*temp_sum
    
    for ours in current_node.state[colour] :
        for theirs in current_node.state[other] :
            if adjacacent(ours, theirs) :
                temp_sum += 0.2
                return temp_sum
    
    return temp_sum


def reward(current_node,colour,weights,reward_s):
    if colour == "white":
        if(not current_node.state['black']) :
            
            if(not current_node.state['white']) :
                return 0 # white = 0 black = 0
            else :
                return 1 # white != 0 black = 0
        else :
            if(not current_node.state['white']) :
                return -1 #black != 0 white = 0
            else :
                return m.tanh(evaluation(current_node, colour,weights)) # black != 0 white != 0
    else : # colour = black
        if(not current_node.state['black']) :
            
            if(not current_node.state['white']) :
                return 0 # white = 0 black = 0
            else :
                return -1 # white != 0 black = 0
        else :
            if(not current_node.state['white']) :
                return 1 #black != 0 white = 0
            else :
                return m.tanh(evaluation(current_node, colour,weights)) # black != 0 white != 0
    
def in_bounds(state, stack_num, move,colour):
    if (state[colour][stack_num][1] + move[1] < 0) or (state[colour][stack_num][1] + move[1] > 7) :
        return False
    elif (state[colour][stack_num][2] + move[2] < 0) or (state[colour][stack_num][2] + move[2] > 7) :
        return False
    else:
        if(colour == 'white') :
            other = 'black'
        else :
            other = 'white'
        if(state[other]) :
            for stack in state[other]:
                if(state[colour][stack_num][1] + move[1] == stack[1]) and (state[colour][stack_num][2] + move[2] == stack[2]) :
                    return False
    return True

def adjacacent(stack1, stack2):
    if stack1 == stack2:
        return False
    if sqrt(pow(stack1[1] - stack2[1] ,2) + pow(stack1[2] - stack2[2],2)).real < 2:
        return True
    return False

#stack_num = the ith token in the state, stack_type = colour
def boom(prev_state, stack_num, stack_type):
    new_state = copy.deepcopy(prev_state)
    
    if len(new_state[stack_type]) == 1:
        new_state[stack_type] = None
        
    else:
        del new_state[stack_type][stack_num]
    for type in new_state :
        if new_state[type]:
            for one_stack in new_state[type] :
                if adjacacent(prev_state[stack_type][stack_num], one_stack):
                    if new_state[type] and (one_stack in new_state[type]):
                        new_state = boom(new_state, new_state[type].index(one_stack), type)
    return new_state

def node_move(prev_node, stack_num, move,colour):
    new_state = copy.deepcopy(prev_node.state)
    copied = False
    # if moving all tokens in a stack
    if new_state[colour][stack_num][0] == move[0]:
        new_stack = copy.deepcopy(new_state[colour][stack_num])
        new_state[colour].pop(stack_num)
    # else moving part of stack
    else :
        new_stack = copy.deepcopy(new_state[colour][stack_num])
        new_stack[0] = move[0]
        new_state[colour][stack_num][0] -= move[0]
    
    for i in range(1,3) :
        new_stack[i] += move[i]
    for n in range(len(new_state[colour])) :
        if new_stack[1] == new_state[colour][n][1] and new_stack[2] == new_state[colour][n][2]:
            new_state[colour][n][0] += new_stack[0]
            copied = True
    if copied == False:
        new_state[colour].append(new_stack)

    node_moved = prev_node.state[colour][stack_num]
    return Node(state = new_state, move = move,action = ("MOVE",move[0],(node_moved[1],node_moved[2]),(node_moved[1]+move[1],node_moved[2]+move[2])))

def state_search(current_node,colour,explode):
    listOfNodes = []
    
    if colour == "white":
        opp_colour = "black"
    else:
        opp_colour = "white"

    if current_node.state[colour]:
        for stack_num in range(len(current_node.state[colour])) :
            # generate all possible nodes for single stack
             
            n = current_node.state[colour][stack_num][0] 
            
            # explode move
            if explode == True:
                boom_state = boom(current_node.state, stack_num, colour)
                temp_action = ("BOOM",(current_node.state[colour][stack_num][1],current_node.state[colour][stack_num][2]))
                listOfNodes.append(Node(state = boom_state,child = [],action = temp_action))
                ## i think filtered boom is not functioning properly, as boom states result a lot less often when using it
                ## also as this function calls for opponents moves too, doesn't record chain explosions
            for i in range(1,n+1):
                for j in range(1, n + 1) :
                    # move up by ith tokens
                    if in_bounds(current_node.state, stack_num, [i,0,j],colour) :
                        listOfNodes.append(node_move(current_node, stack_num, [i,0,j],colour))
                    # left i
                    if in_bounds(current_node.state, stack_num, [i,-j,0],colour) :
                        listOfNodes.append(node_move(current_node, stack_num, [i, -j, 0],colour))
                    # right i
                    if in_bounds(current_node.state, stack_num, [i,j,0],colour) :
                        listOfNodes.append(node_move(current_node, stack_num, [i, j, 0],colour))
                    # down i
                    if in_bounds(current_node.state, stack_num, [i,0,-j],colour) :
                        listOfNodes.append(node_move(current_node, stack_num, [i, 0, -j],colour))
    #shuffling list of possible states so it doesnt always go for the first option
    if colour == 'black' :
        listOfNodes.reverse()
    else :
        random.shuffle(listOfNodes)
    return listOfNodes


# we are maxPlayer hence starts with mPlayer = true, a = -1000, b = 1000
# beta is the maximum score the minimizing player (opponent) can get
def minimax(maxPlayer, current_node, alpha, beta, our_colour,weights,reward_s) : 
    maxNum = 1000
    minNum = -1000
    
    if len(current_node.child) == 0 :
        return reward(current_node, our_colour,weights,reward_s), current_node
    
    if maxPlayer:
        best = minNum
        for child in current_node.child :
            val, temp = minimax(False, child, alpha, beta, our_colour,weights,reward_s)
            if(val > best) :
                best = val
                best_node = child
                alpha = max(alpha, best)
            
            if beta <= alpha :
                break
        return best, best_node
    
    else:
        best = maxNum
        for child in current_node.child :
            val, temp = minimax(True, child, alpha, beta, our_colour,weights,reward_s)
            if(val < best) :
                best = val
                best_node = child
                beta = min(beta, best)
        
            if beta <= alpha :
                break
        return best, best_node


def generateMoves(root, maxDepth, curDepth, colour, explode) :
    curNode = root
    if colour == 'white' :
        oppColour = 'black'
    else :
        oppColour = 'white'
    while curDepth < maxDepth :
        if len(curNode.child) > 0 :
            curDepth += 1
            for child in curNode.child :
                generateMoves(child, maxDepth, curDepth, oppColour, explode)
        else :
            # check if game state is over
            if curNode.state[colour] :
                curNode.child = state_search(curNode, colour, explode)
            else :
                curDepth += 1
    return 0


# leafs an array of tuples: [(node, weight)...]
# generate a fraction of our possible moves from a set of leaf nodes


"""
def someOurMoves(leafs, colour, explode, curSpace, maxSpace, fraction, weights, state_reward) :
    newLeafs = []
    returnLeafs = []
    if len(leafs) > 0 :
        for i in range(len(leafs)) :
            if len(newLeafs)*fraction >= 2 :
                curSpace += int(branch_approximation(leafs[i], colour)*fraction)
            else :
                curSpace += branch_approximation(leafs[i], colour)
            if curSpace <= maxSpace :
                
                leafs[i].child = state_search(leafs[i], colour, explode)
                for j in leafs[i].child :
                    newLeafs.append((j, reward(j, colour, weights, state_reward)))
                newLeafs.sort(key = lambda x: x[1], reverse = True)
                if len(newLeafs)*fraction >= 2 :
                    oldLeafs = newLeafs[int(len(newLeafs)*fraction):]
                else :
                    oldLeafs = []
                for j in oldLeafs :
                    leafs[i].child.remove(j[0])
                returnLeafs += leafs[i].child
                newLeafs = []
            else :
                break
    return returnLeafs, curSpace


"""
def someOurMoves(leafs, colour, explode, curSpace, maxSpace, fraction, weights, state_reward) :
    newLeafs = []
    returnLeafs = []
    oldLeafs = []
    if len(leafs) > 0 :
        for i in range(len(leafs)) :
            if len(newLeafs)*fraction >= 2 :
                curSpace += int(branch_approximation(leafs[i], colour)*fraction)
            else :
                curSpace += branch_approximation(leafs[i], colour)
            if curSpace <= maxSpace :
                
                leafs[i].child = state_search(leafs[i], colour, explode)
                for j in leafs[i].child :
                    newLeafs.append((j, reward(j, colour, weights, state_reward)))
                newLeafs.sort(key = lambda x: x[1], reverse = True)
                if len(leafs[i].child)*fraction >= 2 :
                    oldLeafs += newLeafs[int(len(newLeafs)*fraction):]
                newLeafs = []
            else :
                break
    for i in oldLeafs :
        del(i)
    for i in leafs :
        returnLeafs += i.child
    return returnLeafs, curSpace



def someTheirMoves(leafs, colour, curSpace, maxSpace, weights, state_reward) :
    newLeafs = []
    #print("new call")
    if len(leafs) > 0 :
        for i in leafs :
            curSpace += branch_approximation(i, colour)
            if curSpace <= maxSpace :
                #if len(i[0].child) == 0 :
                i.child = state_search(i, colour, True)
                for j in i.child :
                    newLeafs.append(j)
                    #print(f"opponent: {colour} {j.action}")
            else :
                break
    return newLeafs, curSpace




