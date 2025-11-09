from typing import Union
from game.question_node import QuestionNode
from game.interaction import Interaction
from data.parsing import Parsing
from api.animal_info import AnimalInfo
from game.player import Player

class EndGame:
    def __init__(
        self, filename_or_parsing: Union[str, Parsing], root: QuestionNode, player: Player = None
    ) -> None:
        self.interaction: Interaction = Interaction()
        if isinstance(filename_or_parsing, Parsing):
            self.parsing: Parsing = filename_or_parsing
        else:
            self.parsing: Parsing = Parsing(filename_or_parsing)
        self.root: QuestionNode = root
        self.info: AnimalInfo = AnimalInfo()
        self.player: Player = player

    def end_game(self, node: QuestionNode) -> None:
        final_answer: str = self.interaction.requestInput(
            f"Is it a {node.value}? (true/false)", "bool"
        )
        if final_answer == "true":
            print("Yay! I guessed it right!")
            print("Here some infos about this animal from Wikipedia :")
            print(self.info.get_animal_info(node))
            # Record victory and points
            if self.player:
                self.player.score.victory()
                print(f"\n✅ Victory! You earned {self.player.score.actual_score} points!")
        else:
            self._improve_game(node)

    def _improve_game(self, node: QuestionNode) -> None:
        correct_animal: str = self.interaction.requestInput(
            "Oh no! What was your animal? ", "str"
        )
        new_question: str = self.interaction.requestInput(
            f"Give me a question that distinguishes a {correct_animal} from a {node.value}: ",
            "str",
        )
        answer: str = self.interaction.requestInput(
            f"For a {correct_animal}, what is the answer to your question? (true/false)",
            "bool",
        )

        new_node: QuestionNode = QuestionNode(new_question)
        yes_node: QuestionNode = QuestionNode(correct_animal)
        no_node: QuestionNode = QuestionNode(node.value)

        if answer == "true":
            new_node.yes = yes_node
            new_node.no = no_node
        else:
            new_node.yes = no_node
            new_node.no = yes_node

        node.value = new_node.value
        node.yes = new_node.yes
        node.no = new_node.no

        print("Got it! I'll remember that for next time.")
        self.parsing.save_json_tree(self.root)
        
        if self.player:
            self.player.score.game_over()
            print(f"\n❌ Game Over! You lost {self.player.score.actual_score} points!")
