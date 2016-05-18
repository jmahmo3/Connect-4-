class ConnectFour(object):
    def __init__(self):
        # Initialize an empty board
        self.board = [[None for col in range(7)] for row in range(6)]

    def get_position(self, row, column):
        """
        Returns either None or an integer 1 or 2 depending on which player
        is occupying the given row or column.  Row is an integer between 0
        and 5 and column is an integer between 0 and 6.
        """
        assert row >= 0 and row < 6 and column >= 0 and column < 7
        return self.board[row][column]

    def match_in_direction(self, row, column, step_row, step_col):
        """
        Counts how many chips, starting from (row, column) and moving in the
        direction (step_row, step_col), match the player who occupies (row,column).

        Arguments:
        row: an integer between 0 and 5
        column: an integer between 0 and 6
        step_row: an integer, either -1, 0, or 1
        step_col: an integer, either -1, 0, or 1

        This function first checks which player occupies (row,column).  If no
        player occupies this position, 0 is returned.  Otherwise, the function
        then continues checking (row + step_row, column + step_column), (row +
        2*step_row, column + 2*step_column), and so forth, continuing until a
        location is either empty, the board edge is reached, or a position is
        occupied by an opposing player.  The function then returns how many
        chips (including the first chip at (row, column), match.  Note if the
        function returns 4 or more, this is a winning position. 
        """
        assert row >= 0 and row < 6 and column >= 0 and column < 7
        assert step_row != 0 or step_col != 0 # (0,0) gives an infinite loop

        count = 0
        orig = self.board[row][column]
        if orig == None:
            return 0
        while row >= 0 and row < 6 and column >= 0 and column < 7:
            if self.board[row][column] != orig:
                return count
            row += step_row
            column += step_col
            count += 1
        return count

    def is_game_over(self):
        """
        Returns None if the game is not yet over, or 1 or 2 depending
        on if player 1 or 2 has one the game.
        """
        # Note, match_in_direction is very helpful.
        for row in range(6):
            for column in range(7):
                for (step_row, step_col) in [ (1,0), (0,1), (1,1), (1,-1) ]:
                    if self.match_in_direction(row, column, step_row, step_col) >= 4:
                        #print "Winning 4: %i %i %i %i" % (row, column, step_row, step_col)
                        return [row, column, step_row, step_col]
        return None

    def play_turn(self, player, column):
        """ Updates the board so that player plays in the given column.

        player: either 1 or 2
        column: an integer between 0 and 6
        """
        assert player == 1 or player == 2
        assert column >= 0 and column < 7

        for row in range(5,-1,-1):
            if self.board[row][column] != None:
                self.board[row+1][column] = player
                return
        self.board[0][column] = player

    def print_board(self):
        print "-" * 29
        print "| 0 | 1 | 2 | 3 | 4 | 5 | 6 |"
        print "-" * 29
        for row in range(5,-1,-1):
            s = "|"
            for col in range(7):
                p = self.get_position(row, col)
                if p == None:
                    s += "   |"
                elif p == 1:
                    s += " x |"
                elif p == 2:
                    s += " o |"
                else:
                    # This is impossible if the code is correct, should never occur.
                    s += " ! |"
            print s
        print "-" * 29
