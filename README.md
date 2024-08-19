# Checkers Game

This repository contains a Python implementation of a modified Checkers game, designed for two players. The game follows traditional Checkers rules with some variations, allowing for unique gameplay mechanics like king and triple king promotions.

## Game Overview

The `Checkers` class manages the overall game state, including the board and players. It provides methods for creating players, making moves, checking the status of pieces on the board, and determining the winner.

### Checkers Class

The `Checkers` class represents the game itself. It manages the board, players, and game rules. Here are the key methods:

- **`create_player(player_name, piece_color)`**:
  - Creates a player with a specified name and checker piece color ("Black" or "White").
  - Returns the created `Player` object.

- **`play_game(player_name, starting_square_location, destination_square_location)`**:
  - Moves a piece on the board from the starting square to the destination square.
  - Raises exceptions for invalid moves, such as `OutofTurn`, `InvalidSquare`, or `InvalidPlayer`.
  - Returns the number of captured pieces, or `0` if no pieces were captured.

- **`get_checker_details(square_location)`**:
  - Returns the details of the checker piece at the specified square location.
  - Raises an `InvalidSquare` exception if the location is invalid.
  - Possible return values: `"Black"`, `"White"`, `"Black_king"`, `"White_king"`, `"Black_Triple_King"`, `"White_Triple_King"`, or `None` if no piece is present.

- **`print_board()`**:
  - Prints the current state of the board as an array.

- **`game_winner()`**:
  - Returns the name of the player who has won the game, or `"Game has not ended"` if the game is still ongoing.

### Player Class

The `Player` class represents a player in the game. It tracks the player's name, piece color, and the number of kings, triple kings, and captured pieces.

- **`get_king_count()`**:
  - Returns the number of king pieces the player has.

- **`get_triple_king_count()`**:
  - Returns the number of triple king pieces the player has.

- **`get_captured_pieces_count()`**:
  - Returns the number of opponent pieces the player has captured.

## Unit Testing

This project includes a file for unit tests called `CheckersGameTester.py`. It contains at least five unit tests that validate the functionality of the `Checkers` and `Player` classes using different assert functions.

## Example Usage

```python
# Initialize the game
game = Checkers()

# Create players
Player1 = game.create_player("Adam", "White")
Player2 = game.create_player("Lucy", "Black")

# Play the game
game.play_game("Lucy", (5, 6), (4, 7))
game.play_game("Adam", (2, 1), (3, 0))

# Get checker details
checker_details = game.get_checker_details((3, 1))

# Get captured pieces count
captured_count = Player1.get_captured_pieces_count()
