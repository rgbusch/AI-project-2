import math as m
from f_AI_lure import player_functions as pf

state_evaluation = []

class Node:
    def __init__(self, state=None,child = [], action = None):
        self.state = state 
        self.child = child
        self.action = action


class Tree:
    def __init__(self, root = None, weights = None):
        self.root = root
        self.weights = weights


class Player:
    def __init__(self, colour):
        
        self.colour = colour
        self.move = None
        # used for weight update, save (tiny amount) time by just creating array of values
        """
        f = open("your_team_name/weights.txt","r")
        temp_str = f.read()
        weights = temp_str.strip().split(",")
        for w in range(len(weights)):
            weights[w] = float(weights[w])
        f.close()
        """
        weights = [1.0,1.9230769230769231,2.8461538461538463,3.769230769230769,4.6923076923076925,5.615384615384615,6.538461538461538,7.461538461538462,8.384615384615385,9.307692307692308,10.23076923076923,11.153846153846153]
        # create initial state
        initial_state = {"white":[],"black":[]}
        for i in range(8) :
            if i != 2 and i != 5:
                for j in range(2):
                    initial_state["white"].append([1,i,j])
                for k in range(6,8):
                    initial_state["black"].append([1,i,k])
        root_node = Node(initial_state)
        minimax_tree = Tree(root_node, weights = weights)
        self.minimax_tree = minimax_tree
        
        # if we start as white, generate basic tree here
        # also define opening moves for each colour here
        if colour == "white" :
            pf.generateMoves(self.minimax_tree.root, 2, 0, colour, False)
            if colour == 'white' :
                self.move = [("MOVE",1,(4,1),(3,1)), ("MOVE",2,(3,1),(3,3))]
        else :
            self.move = [("MOVE",1,(7,6),(6,6)), ("MOVE",2,(6,6),(6,4))]


    def action(self):
        # if an opening move, return from list
        if len(self.move) > 0 :
            return self.move.pop(0)
        
        # apply minimax to get the next move
        score,best_node = pf.minimax(True, self.minimax_tree.root, -1000, 1000, self.colour,self.minimax_tree.weights)

        # recording evaluation score of best leaf node
        # arctangent applied to reverse reward score and 0.0000001 being added or subtracted due to range of arctangent function
        """
        if score == 1: 
            score = score - 0.0000001
        elif score == -1:
            score = score + 0.0000001
        state_evaluation.append(m.atanh(score))
        """
        return best_node.action


    def update(self, colour, action):
        actionNotFound = True
        # look for given action in current tree, and assign new root
        if len(self.minimax_tree.root.child) > 0 :
            for node in self.minimax_tree.root.child :
                if(node.action == action) :
                    self.minimax_tree.root = node
                    actionNotFound = False
        
        # if action not found, recreate tree using root + action
        # if starting as black, this will always occur after first white action
        if actionNotFound :
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
        
        # if an opening move, don't generate tree
        if len(self.move) > 0 :
            return
        
        # if the last move was opponents (our move next) generate the tree
        if colour != self.colour :
            curNodes = 1
            # the first few moves in the program seem to take more memory than calculated, so set to 10000
            maxNodes = 12000 
            fraction = 1
            depth = 0
            leafs = [self.minimax_tree.root]
            self.minimax_tree.root.child = []
            
            while curNodes < maxNodes and depth < 14 :
                # if at depth 2, fraction to ~4-7 nodes per state
                if depth > 0 : 
                    temp = pf.branch_approximation(self.minimax_tree.root, self.colour)
                    if temp >= 60 : # rarely gets here
                        fraction = 4/10
                    elif temp >= 40 : # usually here
                        fraction = 6/10
                    elif temp >= 20 :
                        maxNodes = 14000
                        fraction = 8/10
                    else:
                        fraction = 1
                    # only generate moves if can also generate some opponents moves
                    if curNodes + pf.branch_approximation(self.minimax_tree.root, self.colour)*fraction * pf.branch_approximation(self.minimax_tree.root, colour) > maxNodes :
                        break
                leafs, curNodes = pf.someOurMoves(leafs, self.colour, True, curNodes, maxNodes, fraction, self.minimax_tree.weights)
                depth += 1
                if curNodes > maxNodes :
                    break
                leafs, curNodes = pf.someTheirMoves(leafs, colour, curNodes, maxNodes, self.minimax_tree.weights)
                depth += 1
                
            # recording the evaluation score of the best leaf found at a given state
            # used for TDL weight updating
            """
            score,best_node = pf.minimax(True, self.minimax_tree.root, -1000, 1000, self.colour,self.minimax_tree.weights)
            if score == 1: 
                score = score - 0.0000001
            elif score == -1:
                score = score + 0.0000001
            state_evaluation.append(m.atanh(score))
            """
        # weight updating attempted at the end of a game 
        # discarded as weight becomes negatively large after update.
        """
        if colour == self.colour:
            if pf.game_evaluation(self.minimax_tree.root,colour) == True:
                pf.weight_update(state_evaluation,0.1,1,self.minimax_tree.weights)
        """
        