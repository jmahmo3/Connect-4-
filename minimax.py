from connectfour import *
from player import *
from utility import *

class MinimaxNode(ConnectFour):

    @staticmethod
    def init_root(copyfrom, nodeplayer):
        """
        Creates a new instance of the MinimaxNode class, with the board state copied
        from the copyfrom object, which is an instance of the ConnectFour class.  
        
        Also, create two properties:
        * a nodeplayer property, storing the fact that this node is a play for nodeplayer.
        * a from_parent_column property set to None (see below).  This marks that the
          node did not come from a parent.

        This method should only be used to create the root of the game tree from
        the current board state.
        """
        node = MinimaxNode()
        # TODO: set node property storing the board by copying from copyfrom.
        # Be careful about copying. You must copy the lists you are using for storage.
        node.board = [[copyfrom.get_position(row, col) for col in range(7)] for row in range(6)]
        node.nodeplayer = nodeplayer
        node.from_parent_column = None
        return node

    @staticmethod
    def init_child(parent, playcolumn):
        """
        Creates a MinimaxNode by copying the board state from parent (which is an instance
        of MinimaxNode) and then making a play in playcolumn (which is an integer
        between 0 and 6).

        Also, create two properties:
        * nodeplayer property, which is the opposite of the parent nodeplayer, representing
          that the child is now a play for the other player.
        * from_parent_column property, which stores the playcolumn parameter.  This is used to
          know which column was played to to get from the parent to the child, and is used
          at the very end to know which play to make.
        """
        node = MinimaxNode()
        # TODO: set node property storing the board by copying from parent
        node.board = [[parent.get_position(row, col) for col in range(7)] for row in range(6)]
        node.play_turn(parent.nodeplayer, playcolumn)
        node.nodeplayer = 3 - parent.nodeplayer
        node.from_parent_column = playcolumn
        return node

    def compute_children(self):
        """
        Computes the list of children of this node and stores it in a property called children.
        This method only creates the immediate children (this is lazy evaluation).
        """
        # Iterate the non-full columns, createing a new node for each.
        self.children = []
        for col in range(7):
            if self.get_position(5, col) == None:
                self.children.append(MinimaxNode.init_child(self, col))

    def set_minimax_value(self, val):
        """
        Stores the minimax value for this node.  This represents the largest utility
        that can be forced on a leaf no matter how the enemy plays.
        """
        self.value = val

    def get_minimax_value(self):
        """
        From this node, it is possible to reach a leaf with this utility.
        """
        return self.value

class MinimaxPlayer(Player):
    def __init__(self, playernum, ply_depth, utility):
        super(MinimaxPlayer, self).__init__(playernum)
        self.ply_depth = ply_depth
        self.utility = utility

    def minimax(self, node, cur_depth):
        """
        This is the recursive procedure for minimax.  It computes the number N where
        N is the best utlity that can be forced on a leaf.  This value N is stored
        in the tree node by calling set_minimax_value and is also returned from this
        method.
        
        The cur_depth is used to distinguish min/max nodes and the recursion ends
        once cur_depth equals self.ply_depth
        """
        # The code should be similar but simpler than the code in Day 12

        if cur_depth == self.ply_depth:
            u = self.utility.compute_utility(node, self.playernum)
            node.set_minimax_value(u)
            return u

        node.compute_children()

        if cur_depth % 2 == 0: # Max node
            v = -5000000
            for child in node.children:
                v = max(v, self.minimax(child, cur_depth + 1))
            node.set_minimax_value(v)
            return v

        else: # min node
            v = 5000000
            for child in node.children:
                v = min(v, self.minimax(child, cur_depth + 1))
            node.set_minimax_value(v)
            return v

    def play_turn(self, board):
        root = MinimaxNode.init_root(board, self.playernum)
        childval = self.minimax(root, 0)
        print "Completed with val %i" % childval
        for child in root.children:
            if child.get_minimax_value() == childval:
                board.play_turn(self.playernum, child.from_parent_column)
                return

        assert False
