import math as m
from your_team_name import player_functions as pf

state_reward = []

class Node:
    def __init__(self,state=None,child = [],action = None,move = None,depth = None):

        self.state = state 
        self.child = child
        self.move = move
        self.action = action
        self.depth = depth
    
    def hasChild(self):
        return self.child

    def insertChild(self,child_node):
        self.child.append(child_node)



class Tree:
    def __init__(self,root = None,current_depth = None,depth = None,weights = None):
        self.root = root
        self.current_depth=current_depth
        self.depth = depth
        self.weights = weights
    
    def getLeafNodes(self, node, leafs, colour, weights) :
        if node is not None :
            if len(node.child) == 0 :
                leafs.append(node)
            for n in node.child :
                self.getLeafNodes(n, leafs, colour, weights)



class Player:
    def __init__(self, colour):
        
        self.colour = colour
        self.count = 0
        f = open("your_team_name/weights.txt","r")
        
        temp_str = f.read()
        weights = temp_str.strip().split(",")
        for w in range(len(weights)):
            weights[w] = float(weights[w])
        f.close()

        initial_state = {"white":[],"black":[]}
        for i in range(8) :
            if i != 2 and i != 5:
                for j in range(2):
                    initial_state["white"].append([1,i,j])
                for k in range(6,8):
                    initial_state["black"].append([1,i,k])


        root_node = Node(initial_state,depth=0)
        minimax_tree = Tree(root_node,0,2, weights = weights)
        self.minimax_tree = minimax_tree
        
        #if we start as white, generate moveset here  
        if colour == "white" :
            pf.generateMoves(self.minimax_tree.root, 2, 0, colour, True) 

    def action(self):
        
        score,best_node = pf.minimax(True, self.minimax_tree.root, -1000, 1000, self.colour,self.minimax_tree.weights)
        state_reward.append(score)
        return best_node.action
        

#################### NOTES ###################
# BOOM move should provide ~+0.01 to a move, to encourage even trades ie. 2 stacks for 2 stacks
# rewrite order in state_search depending on colour -> white should be BOOM, up, right/left, down
#                                                   -> black should be BOOM, down, left/right, up
##############################################

    def update(self, colour, action):
        
        actionNotFound = True
        # look for given action in current tree, and assign new root
        if colour != self.colour:
            score,best_node = pf.minimax(True, self.minimax_tree.root, -1000, 1000,colour,self.minimax_tree.weights)
            state_reward.append(score)
        
        if len(self.minimax_tree.root.child) > 0 :
            for node in self.minimax_tree.root.child :
                if(node.action == action) :
                    self.minimax_tree.root = node
                    actionNotFound = False
        
        # if action not found, recreate tree using root + action
        # if starting as black, this will always occur after first white action
        boom = False
        if actionNotFound :
            #print(self.minimax_tree.root.state) ## add checking for boom action
            if action[0] == 'BOOM' :
                pf.generateMoves(self.minimax_tree.root, 2, 0, self.colour, True)
                if len(self.minimax_tree.root.child) > 0 :
                    for node in self.minimax_tree.root.child :
                        if(node.action == action) :
                            self.minimax_tree.root = node
            else :
                for j in self.minimax_tree.root.state[colour] :
                    if j[1] == action[2][0] and j[2] == action[2][1] :
                        stack_num = self.minimax_tree.root.state[colour].index(j)
                        move = [None, None, None]
                        move[0] = action[1]
                        move[1] = action[3][0] - action[2][0]
                        move[2] = action[3][1] - action[2][1]
                self.minimax_tree.root = pf.node_move(self.minimax_tree.root, stack_num, move, colour)
            pf.generateMoves(self.minimax_tree.root, 2, 0, self.colour, True)

        if colour != self.colour :
            curNodes = 1
            maxNodes = 16000
            fraction = 1
            count1 = 0
            leafs = [self.minimax_tree.root]
            while curNodes < maxNodes and count1 < 8 :
                count1+= 1
                if count1 > 1 :
                    if pf.branch_approximation(self.minimax_tree.root, self.colour) > 30 :
                        fraction = 1/(8*count1) ##doesn't work well for low stacks. have closer to 1 for low stacks
                    else :
                        fraction = 1/3
                leafs, curNodes = pf.someOurMoves(leafs, self.colour, True, curNodes, maxNodes, fraction, self.minimax_tree.weights)
                if curNodes > maxNodes :
                    break
                leafs, curNodes = pf.someTheirMoves(leafs, colour, curNodes, maxNodes)
    
            score,best_node = pf.minimax(True, self.minimax_tree.root, -1000, 1000, self.colour,self.minimax_tree.weights)
            state_reward.append(score)
        
        # checks if the game state after updating has the game completed, if completed, update the weight
        if pf.game_evaluation(self.minimax_tree.root,colour) == True:
            pf.weight_update(state_reward,0.1,1,self.minimax_tree.weights)
        