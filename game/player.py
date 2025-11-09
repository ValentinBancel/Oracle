import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from scoring.score import Score


class Player:
    username: str
    score: Score

    def __init__(self, username: str, score: Score) -> None:
        self.username = username
        self.score = score
