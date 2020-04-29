import math as m
from your_team_name import player_functions as pf

class Node:
    def __init__(self,state=None,child = [],action = None,move = None,depth = None,weights = None):

        self.state = state
        self.child = child
        self.move = move
        self.action = action
        self.depth = depth
        self.weights = weights

    
    def hasChild(self):
        return self.child

    def insertChild(self,child_node):
        self.child.append(child_node)

class Tree:
    def __init__(self,root = None,current_depth = None,depth = None):
        self.root = root
        self.current_depth=current_depth
        self.depth = depth
    
    



class Player:
    def __init__(self, colour):
        """
        This method is called once at the beginning of the game to initialise
        your player. You should use this opportunity to set up your own internal
        representation of the game state, and any other information about the 
        game state you would like to maintain for the duration of the game.

        The parameter colour will be a string representing the player your 
        program will play as (White or Black). The value will be one of the 
        strings "white" or "black" correspondingly.
        """
        self.colour = colour 
        self.opening_moves = {}

        
        #we make move first
        if colour =="white": 

            initial_state = {"white":[],"black":[]}
            for i in range(8) :
                if i != 2 and i != 5:
                    for j in range(2):
                        initial_state["white"].append([1,i,j])
                    for k in range(6,8):
                        initial_state["black"].append([1,i,k])


            root_node = Node(initial_state,depth=0)
            minimax_tree = Tree(root_node,0,2)
            self.minimax_tree = minimax_tree
            #white always start first
            
            initial_possible_moves = pf.state_search(minimax_tree.root,'white',False)
            
            for child in initial_possible_moves:
                child.depth = 1
            minimax_tree.root.child = initial_possible_moves
            minimax_tree.current_depth += 1
            current_nodes = minimax_tree.root.child

            opponent_colour = "black"
            
            while minimax_tree.current_depth != minimax_tree.depth :
                temp_list = []
                if (current_nodes[0].depth % 2) == 0:
                    for x in current_nodes:
                        x.child = pf.state_search(x,colour,False)
                        for y in x.child: # can save time if this for is in state_search
                            y.depth = minimax_tree.current_depth + 1
                        temp_list += x.child
                    current_nodes = temp_list
                    minimax_tree.current_depth += 1
                else:
                    for x in current_nodes:
                        x.child = pf.state_search(x,opponent_colour,False)
                        for y in x.child:
                            y.depth = minimax_tree.current_depth + 1
                        temp_list += x.child
                    current_nodes = temp_list
                    minimax_tree.current_depth += 1
                    
        else:
            root_node = Node(depth=0)
            minimax_tree = Tree(root_node,0,2)
            self.minimax_tree = minimax_tree




    def action(self):
        """
        This method is called at the beginning of each of your turns to request 
        a choice of action from your program.

        Based on the current state of the game, your player should select and 
        return an allowed action to play on this turn. The action must be
        represented based on the spec's instructions for representing actions.
        """
        
        score,best_node = pf.minimax(True, self.minimax_tree.root, -1000, 1000, self.colour)

        return best_node.action
        
        
        
        
        #return ("BOOM", (0, 0))


    def update(self, colour, action):
        """
        This method is called at the end of every turn (including your player’s 
        turns) to inform your player about the most recent action. You should 
        use this opportunity to maintain your internal representation of the 
        game state and any other information about the game you are storing.

        The parameter colour will be a string representing the player whose turn
        it is (White or Black). The value will be one of the strings "white" or
        "black" correspondingly.

        The parameter action is a representation of the most recent action
        conforming to the spec's instructions for representing actions.

        You may assume that action will always correspond to an allowed action 
        for the player colour (your method does not need to validate the action
        against the game rules).
        """
        
        # change root node to action node
        if(self.minimax_tree.root.state == None) :
            initial_state = {"white":[],"black":[]}
            for i in range(8) :
                if i != 2 and i != 5:
                    for j in range(2):
                        initial_state["white"].append([1,i,j])
                    for k in range(6,8):
                        initial_state["black"].append([1,i,k])
                                    
            for j in initial_state["white"] :
                if j[1] == action[2][0] and j[2] == action[2][1] :
                    print('here')
                    print(j)
                    print(action)
                    stack_num = initial_state["white"].index(j)
                    list = [None, None, None]
                    list[0] = 1
                    list[1] = action[3][0] - j[1]
                    list[2] = action[3][1] - j[2]
            self.minimax_tree.root.state = initial_state
            self.minimax_tree.root = pf.node_move(self.minimax_tree.root, stack_num, list, 'white')
            self.minimax_tree.root.child = pf.state_search(self.minimax_tree.root, 'black', False)

            child_set = True
        
        for node in self.minimax_tree.root.child :
            if(node.action == action) :
                self.minimax_tree.root = node
                # maybe update all depths
            
            
        # if was our turn do nothing else, if was theirs generate new nodes
        if(colour != self.colour) :
            if(len(self.minimax_tree.root.child) == 0) :
                self.minimax_tree.root.child = pf.state_search(self.minimax_tree.root, self.colour, True)
            for x in self.minimax_tree.root.child :
                if(len(x.child) == 0) :
                    x.child = pf.state_search(x, colour, True)

            
        # TODO: Update state representation in response to action.
        