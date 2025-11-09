import sys
from game.end_game import EndGame
from game.interaction import Interaction
from game.question_tree import QuestionTree
from game.question_node import QuestionNode
from game.player import Player

class PlayGame:
    def __init__(self, filename: str, username: str) -> None:
        self.question_tree: QuestionTree = QuestionTree(filename)
        self.interaction: Interaction = Interaction()
        self.player: Player = Player(username)
        self.end_game: EndGame = EndGame(filename, self.question_tree.root, self.player)

    def _game_body(self, node: QuestionNode) -> None:
        if node.yes is None and node.no is None:
            self.end_game.end_game(node)
        else:
            answer: str = self.interaction.requestInput(
                f"{node.value} (true/false) ", "bool"
            )
            self.player.score.add_point()
            if answer == "true":
                self._game_body(node.yes)
            else:
                self._game_body(node.no)

    def _play(self) -> None:
        print("Welcome to the 20 Questions Game!")
        print("Try to think of an animal, and I'll guess it.")

        self._game_body(self.question_tree.root)
        
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python main.py <filename> <username>")
        print("Example: python main.py data/animals_tree.json player1")
        sys.exit(1)
    
    game = PlayGame(sys.argv[1], sys.argv[2])
    game._play()
    
    # Display final score
    print(f"\nGame Over, {game.player.username}!")
    print(f"Your score: {game.player.score.actual_score}")
    print(f"Total score: {game.player.score.get_user_score(game.player.username)}")