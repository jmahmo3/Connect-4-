import random

class Player(object):
    def __init__(self, playernum):
        self.playernum = playernum

    def play_turn(self, board):
        """
        This method is passed an instance of ConnectFour.  It should examine the board
        (using methods on the ConnectFour class) and eventually call board.play_turn and return.
        """
        pass

class Human(Player):
    def __init__(self, playernum):
        super(Human,self).__init__(playernum)

    def play_turn(self, board):
        print ""
        print "Player %i" % self.playernum
        board.print_board()
        while True:
            col = input("Enter a col (0-6): ")
            if col >= 0 and col < 7 and board.get_position(5, col) == None:
                board.play_turn(self.playernum, col)
                return

class RandomPlayer(Player):
    def __init__(self, playernum):
        super(RandomPlayer,self).__init__(playernum)

    def play_turn(self, board):
        cols = []
        for col in range(7):
            if board.get_position(5, col) == None:
                cols.append(col)
        board.play_turn(self.playernum, random.choice(cols))
