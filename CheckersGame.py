# Author: Daniel Arevalo
# GitHub Username: DanielArevalo059
# Date: March 19, 2023
# Description: A Checkers game portfolio project


class Checkers:
    """
    Represents the game as played. This Class will create a game board, a player, and
    will have a method for playing the game which moves the players.
    This Class will need to communicate with the Player Class in order to create the Player objects
    and make the Player objects move on the board.
    """

    def __init__(self):
        """___Init__ will create a new game board as an array with pieces placed in correct
        starting spots.

        """
        self._board_game = [
            ["X" if (i + j) % 2 == 0 else "White" for j in range(8)] if i < 3 else
            [None if (i + j) % 2 == 1 else "X" for j in range(8)] if 3 <= i <= 4 else
            ["Black" if (i + j) % 2 == 1 else "X" for j in range(8)]
            for i in range(8)
        ]
        for row in range(8):     #boardgame to contain objects of CheckerPieces
            for col in range(8):
                if self._board_game[row][col] == "White":
                    self._board_game[row][col] = CheckerPiece("White")

                if self._board_game[row][col] == "Black":
                    self._board_game[row][col] = CheckerPiece("Black")


        self._player_1 = None  # Player 1 is initialized as White when Player is created
        self._player_2 = None  # Player 2 is initialized as Black when Player is created

    def create_player(self, player_name, piece_color):
        """
        Sends information to Player Class to create a Player object with the passed name and color. Returns Player object
        """
        if piece_color == "White":
            self._player_1 = Player(player_name, piece_color)
            return self._player_1

        else:
             self._player_2 = Player(player_name, piece_color)
             return self._player_2

    def play_game(self, player_name, starting_square, destination_square):
        """
        Takes the current square of a piece and destination square, and moves pieces. - Must be tuples
        Returns the number of captured pieces, if any. Otherwise, 0 returned
        Crowns the piece a King or Triple King if appropriate
        Assesses whether the piece is a King/TK and moves accordingly
         """
        start_row, start_col = starting_square
        des_row, des_col = destination_square

        try:
            self.validate_move(player_name, start_row, start_col, des_row, des_col, starting_square)
        except InvalidPlayer:
            return "Oops, please enter a valid name."
        except OutofTurn:
            return "Oops, not your turn! Please let your opponent make a move."
        except InvalidSquare:
            return "That is an invalid square. Please try again."

        #initialize the player for this turn
        if self._player_1.get_player_name() == player_name:
            current_player = self._player_1
            opponent = self._player_2

        else:
            current_player = self._player_2
            opponent = self._player_1

        checker_piece = self._board_game[start_row][start_col]
        checker_rank = checker_piece.get_rank()
        king_rank = current_player.get_player_color() + "_King"

        if checker_rank == current_player.get_player_color(): #check if CheckerPiece is basic rank
            captured_pieces = self.basic_rank_move(checker_piece, start_row, start_col, des_row, des_col, current_player, opponent)

        elif checker_rank == king_rank:                       #check if CheckerPiece is King
            captured_pieces = self.king_rank_move(checker_piece, start_row, start_col, des_row, des_col, current_player, opponent)

        else:       #else CheckerPiece is Triple_King
            captured_pieces = self.triple_rank_move(checker_piece, start_row, start_col, des_row, des_col, current_player, opponent)



        if captured_pieces > 0:
            current_player.set_captured_pieces_count(captured_pieces)
            current_player.set_prev_turn(True, destination_square)
        else:
            current_player.set_prev_turn(False, destination_square)
        return captured_pieces


    def basic_rank_move(self, checker_piece, start_row, start_col, des_row, des_col, current_player, opponent):
        """Returns the captured by a basic CheckerPiece being moved"""
        row_moved = start_row - des_row
        col_moved = start_col - des_col
        current_player.set_turn(False)
        opponent.set_turn(True)

        if abs(row_moved) == 1:   #No jump is occurring
            self._board_game[start_row][start_col] = None  # Clear start location to None
            self._board_game[des_row][des_col] = checker_piece  # Set new destination for Checker
            if des_row == 0 or des_row == 7:
                print(f"{current_player.get_player_name()}, you have been kinged!")
                current_player.set_king_count(1)
                checker_piece.set_rank("_King")
            return 0

        else:       #Jump is occurring
            if row_moved < 0: #calculate White moving down

                if col_moved > 1:                                           #White moving down and left
                    self._board_game[start_row][start_col] = None           #Clear start location to None
                    self._board_game[des_row][des_col] = checker_piece      #Set new destination for Checker
                    captured_piece = self._board_game[start_row + 1][start_col - 1]
                    self._board_game[start_row + 1][start_col - 1] = None #remove jumped checker from board

                if col_moved < 1:                                           #White moving down and right
                    self._board_game[start_row][start_col] = None
                    self._board_game[des_row][des_col] = checker_piece
                    captured_piece = self._board_game[start_row + 1][start_col + 1]
                    self._board_game[start_row + 1][start_col + 1] = None

                   #Check if king or triple king was captured, update count
                if "_Triple_King" in captured_piece.get_rank():
                    opponent.set_triple_king_count(-1)

                elif "_King" in captured_piece.get_rank():
                    opponent.set_king_count(-1)

                #Check if White is kinged on a capture
                if des_row == 7:
                    print(f" {current_player.get_player_name}, you have been kinged!")
                    current_player.set_king_count(1)
                    checker_piece.set_rank("_King")
                    return 1
                #Following code not implemented in this assignment
                # #check if white has another move
                # if self._board_game[des_row+1][des_col-1] != None:
                #     if self._board_game[des_row+1][des_col-1].get_checker_color() == opponent.get_player_color() and self._board_game[des_row+2][des_col-2] == None:
                #         print("You have one more jump available. Please take another turn.")
                #         current_player.set_turn(True)          #current player has another move
                #         opponent.set_turn(False)
                #
                # if self._board_game[des_row+1][des_col+1] != None:
                #     if self._board_game[des_row+1][des_col+1].get_checker_color() == opponent.get_player_color() and self._board_game[des_row+2][des_col+2] == None:
                #         print("You have one more jump available. Please take another turn.")
                #         current_player.set_turn(True)          #current player has another move
                #         opponent.set_turn(False)

            else:               #Black is moving up
                if col_moved > 1:  #Black moving up and left
                    self._board_game[start_row][start_col] = None  # Clear start location to None
                    self._board_game[des_row][des_col] = checker_piece  # Set new destination for Checker
                    captured_piece = self._board_game[start_row - 1][start_col - 1]
                    self._board_game[start_row - 1][start_col - 1] = None  # remove jumped checker from board

                if col_moved < 1:  # Black moving up and right
                    self._board_game[start_row][start_col] = None
                    self._board_game[des_row][des_col] = checker_piece
                    captured_piece = self._board_game[start_row - 1][start_col + 1]
                    self._board_game[start_row - 1][start_col + 1] = None

                #check if king or triple king was captured, update count
                if "_Triple_King" in captured_piece.get_rank():
                    opponent.set_triple_king_count(-1)

                elif "_King" in captured_piece.get_rank():
                    opponent.set_king_count(-1)

                    # Check if Black is kinged on a capture
                if des_row == 0:
                    print("You have been kinged!")
                    current_player.set_king_count(1)
                    checker_piece.set_rank("_King")
                    return 1

                #Following code not implemented in this assignment
                # # check if Black has another move
                # if self._board_game[des_row - 1][des_col + 1] != None:
                #     if self._board_game[des_row - 1][des_col + 1].get_checker_color() == opponent.get_player_color() and self._board_game[des_row - 2][des_col + 2] == None:
                #         print("You have one more jump available. Please take another turn.")
                #         current_player.set_turn(True)
                #         opponent.set_turn(False)
                #
                # if self._board_game[des_row - 1][des_col - 1] != None:
                #     if self._board_game[des_row - 1][des_col - 1].get_checker_color() == opponent.get_player_color() and self._board_game[des_row - 2][des_col - 2] == None:
                #         print("You have one more jump available. Please take another turn.")
                #         current_player.set_turn(True)
                #         opponent.set_turn(False)

        return 1



    def king_rank_move(self, checker_piece, start_row, start_col, des_row, des_col, current_player, opponent):
        """Returns the captured pieces by a king CheckerPiece being moved"""
        row_moved = start_row - des_row
        col_moved = start_col - des_col
        current_player.set_turn(False)
        opponent.set_turn(True)

        if abs(row_moved) == 1:   #No capture is occurring
            self._board_game[start_row][start_col] = None  # Clear start location to None
            self._board_game[des_row][des_col] = checker_piece  # Set new destination for Checker
            if current_player.get_player_color() == "White" and des_row == 0:                 #check if White triple kinged
                print(f"{current_player.get_player_name()}, you have been triple kinged!")
                current_player.set_triple_king_count(1)
                checker_piece.set_rank("_Triple_King")
            if current_player.get_player_color == "Black" and des_row == 7:                 #check if Black triple kinged
                print(f"{current_player.get_player_name()}, you have been triple kinged!")
                current_player.set_triple_king_count(1)
                checker_piece.set_rank("_Triple_King")
            return 0

        else:           #piece is being captured

            # CheckerPiece moving down & right
            if row_moved < 0 and col_moved < 0:
                col = start_col + 1
                for row in range(start_row+1, des_row):
                    if self._board_game[row][col] != None:
                        captured_piece = self._board_game[row][col]
                        self._board_game[row][col] = None
                    col += 1

            #CheckerPiece is moving down & left
            if row_moved < 0 and col_moved > 0:
                col = start_col - 1
                for row in range(start_row + 1, des_row):
                    if self._board_game[row][col] != None:
                        captured_piece = self._board_game[row][col]
                        self._board_game[row][col] = None
                    col -= 1

            # CheckerPiece moving up & right
            if row_moved > 0 and col_moved < 0:
                col = start_col + 1
                for row in range(start_row - 1, des_row, -1):
                    if self._board_game[row][col] != None:
                        captured_piece = self._board_game[row][col]
                        self._board_game[row][col] = None
                    col += 1

            #CheckerPiece moving up & left
            if row_moved > 0 and col_moved > 0:
                col = start_col - 1
                for row in range(start_row - 1, des_row, -1):
                    if self._board_game[row][col] != None:
                        captured_piece = self._board_game[row][col]
                        self._board_game[row][col] = None
                    col -= 1

            #check if captured piece was king or triple king, update count
            if opponent.get_player_color() + "_Triple_King" == captured_piece.get_rank():
                opponent.set_triple_king_count(-1)

            if opponent.get_player_color() + "_King" == captured_piece.get_rank():
                opponent.set_king_count(-1)

            #set new destination, clear old location
            self._board_game[start_row][start_col] = None
            self._board_game[des_row][des_col] = checker_piece

            if checker_piece.get_checker_color() == "White" and des_row == 0:                 #check if White triple kinged
                print(f"{current_player.get_player_name()}, you have been triple kinged!")
                current_player.set_triple_king_count(1)
                checker_piece.set_rank("_Triple_King")
                return 1
            elif checker_piece.get_checker_color() == "Black" and des_row == 7:                 #check if Black triple kinged
                print(f"{current_player.get_player_name()}, you have been triple kinged!")
                current_player.set_triple_king_count(1)
                checker_piece.set_rank("_Triple_King")
                return 1

            #Below code not implemented in assignment
            #Check if further king captures are available. If king_capture_available returns true, then current_player.turn = true, opponent.turn = false
            # if self.king_capture_available(checker_piece, des_row, des_col, current_player, opponent):
            #     print("You have another jump available! Please take another turn.")
            #     current_player.set_turn(True)
            #     opponent.set_turn(False)

        return 1

    #Below code not implemented in assignment
    # def king_capture_available(self, checker_piece, des_row, des_col, current_player, opponent):
    #
    #     down_right = True
    #     down_left = True
    #     up_right = True
    #     up_left = True
    #
    #     # Check diagonal down & right
    #     if down_right:
    #         col = des_col + 1
    #         opponent_piece = False
    #         for row in range(des_row + 1, 8):
    #             if col > 7:
    #                 break
    #             if self._board_game[row][col] != None and self._board_game[row][col].get_checker_color() == opponent.get_player_color():
    #                 if opponent_piece == True:
    #                     break
    #                 else:
    #                     opponent_piece = True
    #             if opponent_piece == True and self._board_game[row][col] == None:
    #                 return True
    #             col += 1
    #
    #     # Check diagonal down & left
    #     if down_left:
    #         col = des_col - 1
    #         opponent_piece = False
    #         for row in range(des_row + 1, 8):
    #             if col < 0:
    #                 break
    #             if self._board_game[row][col] != None and self._board_game[row][col].get_checker_color() == opponent.get_player_color():
    #                 if opponent_piece == True:
    #                     break
    #                 else:
    #                     opponent_piece = True
    #             if opponent_piece == True and self._board_game[row][col] == None:
    #                 return True
    #             col -= 1
    #
    #
    #         # Check diagonal up & right
    #     if up_right:
    #         col = des_col + 1
    #         opponent_piece = False
    #         for row in range(des_row - 1, -1, -1):
    #             if col > 7:
    #                 break
    #             if self._board_game[row][col] != None and self._board_game[row][col].get_checker_color() == opponent.get_player_color():
    #                 if opponent_piece == True:
    #                     break
    #                 else:
    #                     opponent_piece = True
    #             if opponent_piece == True and self._board_game[row][col] == None:
    #                 return True
    #             col += 1
    #
    #         # Check diagonal up & left
    #     if up_left:
    #         col = des_col - 1
    #         opponent_piece = False
    #         for row in range(des_row - 1, -1, -1):
    #             if col < 0:
    #                 break
    #             if self._board_game[row][col] != None and self._board_game[row][col].get_checker_color() == opponent.get_player_color():
    #                 if opponent_piece == True:
    #                     break
    #                 else:
    #                     opponent_piece = True
    #             if opponent_piece == True and self._board_game[row][col] == None:
    #                 return True
    #             col -= 1
    #
    #     return False



    def triple_rank_move(self, checker_piece, start_row, start_col, des_row, des_col, current_player, opponent):
        """Returns the captured count by a triple king CheckerPiece being moved"""

        row_moved = start_row - des_row
        col_moved = start_col - des_col
        current_player.set_turn(False)
        opponent.set_turn(True)
        captured_piece_one = None
        captured_piece_two = None

        if abs(row_moved) == 1:  # No capture is occurring
            self._board_game[start_row][start_col] = None  # Clear start location to None
            self._board_game[des_row][des_col] = checker_piece  # Set new destination for Checker
            return 0


        else:           #piece or pieces are being captured

            # CheckerPiece capturing down & right
            if row_moved < 0 and col_moved < 0:
                col = start_col + 1
                captured_count = 0
                for row in range(start_row+1, des_row):
                        if self._board_game[row][col] != None and self._board_game[row][col].get_checker_color() == opponent.get_player_color():
                            captured_piece_one = self._board_game[row][col]
                            self._board_game[row][col] = None
                            captured_count = 1
                            if self._board_game[row+1][col+1] != None:
                                captured_piece_two = self._board_game[row+1][col+1]
                                self._board_game[row + 1][col + 1] = None
                                captured_count += 1
                        col += 1

                # CheckerPiece capturing down & left
            if row_moved < 0 and col_moved > 0:
                col = start_col - 1
                captured_count = 0
                for row in range(start_row + 1, des_row):
                    if self._board_game[row][col] != None and self._board_game[row][col].get_checker_color() == opponent.get_player_color():
                        captured_piece_one = self._board_game[row][col]
                        self._board_game[row][col] = None
                        captured_count = 1
                        if self._board_game[row + 1][col - 1] != None:
                            captured_piece_two = self._board_game[row + 1][col - 1]
                            self._board_game[row + 1][col - 1] = None
                            captured_count += 1
                    col -= 1

                # CheckerPiece capturing up & right
            if row_moved > 0 and col_moved < 0:
                col = start_col + 1
                captured_count = 0
                for row in range(start_row - 1, des_row, -1):
                    if self._board_game[row][col] != None and self._board_game[row][col].get_checker_color() == opponent.get_player_color():
                        captured_piece_one = self._board_game[row][col]
                        self._board_game[row][col] = None
                        captured_count = 1
                        if self._board_game[row - 1][col + 1] != None:
                            captured_piece_two = self._board_game[row - 1][col + 1]
                            self._board_game[row - 1][col + 1] = None
                            captured_count += 1
                    col += 1

                # CheckerPiece capturing up & left
            if row_moved > 0 and col_moved > 0:
                col = start_col - 1
                captured_count = 0
                for row in range(start_row - 1, des_row, -1):
                    if self._board_game[row][col] != None and self._board_game[row][col].get_checker_color() == opponent.get_player_color():
                        captured_piece_one = self._board_game[row][col]
                        self._board_game[row][col] = None
                        captured_count = 1
                        if self._board_game[row - 1][col - 1] != None:
                            captured_piece_two = self._board_game[row - 1][col - 1]
                            self._board_game[row - 1][col - 1] = None
                            captured_count += 1
                    col -= 1

        if captured_piece_one != None:

            #check if captured_piece_one was king or triple king, update count
            if opponent.get_player_color() + "_Triple_King" == captured_piece_one.get_rank():
                opponent.set_triple_king_count(-1)

            if opponent.get_player_color() + "_King" == captured_piece_one.get_rank():
                opponent.set_king_count(-1)

        if captured_piece_two != None:

            #check if captured_piece_two was king or triple king, update count
            if opponent.get_player_color() + "_Triple_King" == captured_piece_two.get_rank():
                opponent.set_triple_king_count(-1)

            if opponent.get_player_color() + "_King" == captured_piece_two.get_rank():
                opponent.set_king_count(-1)

        #set new destination, clear old location
        self._board_game[start_row][start_col] = None
        self._board_game[des_row][des_col] = checker_piece

        return captured_count


    def validate_move(self, player_name, start_row, start_col, des_row, des_col, starting_square):
        """
        Validate if player is going out of turn - Raises Exception otherwise
        Validate if the player is playing its own piece - Raises Exception otherwise
        Validate if player moving to valid position - Raises Exception otherwise
        Validate if player name is valid - Raises Exception otherwise
        """
        squares_moved = start_col - des_col

        if self._player_1.get_player_name() != player_name and self._player_2.get_player_name() != player_name:
            raise InvalidPlayer

        elif self._player_1.get_player_name() == player_name:
            current_player = self._player_1
            opponent = self._player_2

        elif self._player_2.get_player_name() == player_name:
            current_player = self._player_2
            opponent = self._player_1

        if abs(squares_moved) > 1:
            if current_player.get_prev_turn_capture() == True and current_player.get_prev_destination() == starting_square:
                opponent.set_turn(False)
                current_player.set_turn(True)

        if opponent.get_turn():
                raise OutofTurn

        if (start_row >= 8 or start_row < 0) or (start_col >= 8 or start_col < 0):
            raise InvalidSquare

        if (des_row >= 8 or des_row < 0) or (des_col >= 8 or des_col < 0):
            raise InvalidSquare

        if self._board_game[start_row][start_col] == "X" or self._board_game[start_row][start_col] == None:
            raise InvalidSquare

        if current_player.get_player_color() != self._board_game[start_row][start_col].get_checker_color(): #if current player does not own the checker trying to move
            raise InvalidSquare

        if self._board_game[des_row][des_col] != None:
            raise InvalidSquare                 #if destination square is not empty, cannot move there

    def game_winner(self):
        """Returns the winner of the game. If no winner yet, returns 'Game has not ended."""
        if  self._player_1.get_captured_pieces_count() == 12:
            return self._player_1.get_player_name()
        elif self._player_2.get_captured_pieces_count() == 12:
            return self._player_2.get_player_name()
        else:
            return "Game has not ended."

    def get_checker_details(self, location):
        """
        Receives location of square and returns the checker details on that square - Black, White, BK, WK, BTK, WTK
        Returns None if square is empty
        Returns InvalidSquare exception if invalid square location
        """
        row, col = location
        if self._board_game[row][col] != None and self._board_game[row][col] != "X":
            return self._board_game[row][col].get_rank()
        else:
            return None
        # return values for checker

    def print_board(self):
        """Returns an array of the current game board status."""

        display_board = []
        for item in self._board_game:
            display_board.append(list(item))

        for row in range(8):     #iterate through boardgame to display color of CheckerPieces
            for col in range(8):
                if display_board[row][col] != "X" and display_board[row][col] != None:
                    display_board[row][col] = display_board[row][col].get_rank()
                else: display_board[row][col] = None

        print(display_board)


class Player:
    """
    Creates a Player object with name, color, current turn, previous turn data,
    and checker piece counts attributes
    """

    def __init__(self, player_name, checker_color):
        """Initializes the Player object name and color. Only white or black"""
        self._player_name = player_name
        self._checker_color = checker_color
        self._captured_count = 0
        self._king_count = 0
        self._triple_king_count = 0
        self._previous_turn_capture = None
        self._dest_location = None
        if checker_color == "Black":
            self._turn = True
        else:
            self._turn = False

    def get_king_count(self):
        """returns how many kings this player has"""
        return self._king_count

    def set_king_count(self, add_to_count):
        """Once a king is gained or lost, the current player's is updated"""
        self._king_count += add_to_count
        return

    def get_triple_king_count(self):
        """Returns how many TKs the player has"""
        return self._triple_king_count

    def set_triple_king_count(self, add_to_count):
        """one a triple king is gained or lost, updates this count"""
        self._triple_king_count += add_to_count
        return

    def get_captured_pieces_count(self):
        """Returns the number of opponent pieces this player captured"""
        return self._captured_count

    def set_captured_pieces_count(self, add_to_count):
        """Sets the captured pieces the player has"""
        self._captured_count += add_to_count
        return

    def get_player_name(self):
        """Returns player name"""
        return self._player_name

    def get_player_color(self):
        """returns player checker color"""
        return self._checker_color

    def get_turn(self):
        """Returns true or false, depending if it is the player's turn"""
        return self._turn

    def set_turn(self,turn_set):
        """Sets the player turn to True or False after each turn"""
        self._turn = turn_set
        return

    def get_prev_turn_capture(self):
        """Sets to True if the player had a capture in the previous turn"""
        return self._previous_turn_capture

    def get_prev_destination(self):
        """Previous destination. Used to validate a double-jump"""
        return self._dest_location

    def set_prev_turn(self, capture, destination):
        """Sets the date members for each previous turn. Used to validate a double-jump turn"""
        self._previous_turn_capture = capture
        self._dest_location = destination
        return


class CheckerPiece:
    """
    Creates a CheckerPiece object with color and rank with appropriate getters and setters.
    """
    def __init__(self, color):
        self._checker_color = color
        self._rank = color

    def get_checker_color(self):
        """Returns the checker color"""
        return self._checker_color

    def get_rank(self):
        """Returns the rank of the CheckerPiece"""
        return self._rank

    def set_rank(self, rank):
        """Sets the rank for the CheckerPiece"""
        self._rank = self._checker_color + rank






    #Exception Classes below:

class InvalidPlayer(Exception):
    pass

class InvalidSquare(Exception):
    pass

class OutofTurn(Exception):
    pass



# def main():
#     pass
#
# if  __name__ == "__main__":
#     main()
