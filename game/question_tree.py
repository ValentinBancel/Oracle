from typing import Optional
from data.parsing import Parsing
from game.question_node import QuestionNode


class QuestionTree:
    def __init__(self, filename: str) -> None:
        self.filename: str = filename
        self.parsing: Parsing = Parsing(filename)
        # En mode strict: ne pas utiliser de racine par défaut, lever une erreur
        # si le fichier ne peut pas être chargé.
        self.root: Optional[QuestionNode] = self.parsing.load_json_tree(
            default=None, verbose=True
        )
