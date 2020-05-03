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
                leafs.append((node, pf.reward(node, colour,self.weights))) # change to append weight too
            for n in node.child :
                self.getLeafNodes(n, leafs, colour, weights)



class Player:
    def __init__(self, colour):
        
        self.colour = colour
        
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
            pf.generateMoves(self.minimax_tree.root, 2, 0, colour, False)




    def action(self):
        
        score,best_node = pf.minimax(True, self.minimax_tree.root, -1000, 1000, self.colour,self.minimax_tree.weights)

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
            for j in self.minimax_tree.root.state['white'] :
                if j[1] == action[2][0] and j[2] == action[2][1] :
                    stack_num = self.minimax_tree.root.state["white"].index(j)
                    move = [None, None, None]
                    move[0] = 1
                    move[1] = action[3][0] - j[1]
                    move[2] = action[3][1] - j[2]
            self.minimax_tree.root = pf.node_move(self.minimax_tree.root, stack_num, move, 'white')
            pf.generateMoves(self.minimax_tree.root, 2, 0, 'black', False)

        # if was our turn do nothing else, if was theirs generate new nodes
        if colour != self.colour :
            depth = 0
            approx1 = pf.branch_approximation(self.minimax_tree.root, colour)
            approx2 = pf.branch_approximation(self.minimax_tree.root, self.colour)
            approx = (approx1 + approx2)/2
            if approx > 5 : # approx <= 5 if one node each can change to 3
                while m.pow(approx, depth + 1) < 10000 : # 20000 gets max memory = 103MB
                    depth += 1
            else :
                depth = 2
            #generate moves to desired depth
            pf.generateMoves(self.minimax_tree.root, depth, 0, self.colour, True)
            
            available = 10000 - approx*depth
            maxNodesToExplore = available/approx
           
            if approx > 5 :
                
                listOfLeafs = []
                self.minimax_tree.getLeafNodes(self.minimax_tree.root, listOfLeafs, self.colour, self.minimax_tree.weights)
                listOfLeafs.sort(key = lambda x: x[1])
                
                # determine how many nodes to explore
                if maxNodesToExplore > len(listOfLeafs) :
                    nodesToExplore = len(listOfLeafs)
                else :
                    nodesToExplore = int(maxNodesToExplore)
                if nodesToExplore > 250 :
                    nodesToExplore = 250
                
                if len(listOfLeafs) > 0 : 
                    for i in range(nodesToExplore) :
                        if depth % 2 == 0 :
                            pf.generateMoves(listOfLeafs[i][0], 1, 0, self.colour, True)
                        else :
                            pf.generateMoves(listOfLeafs[i][0], 1, 0, colour, True)
       
