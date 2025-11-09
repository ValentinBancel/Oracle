from interfaces.i_score_repository import IScoreRepository


class Score:
    repository: IScoreRepository
    username: str
    point_per_question: int = 5
    actual_score: int = 0
    user_score: int = 0

    def __init__(self, username: str, repository: IScoreRepository) -> None:
        self.username = username
        self.repository = repository
        self.repository.user_exists(self.username)
        self.user_score = self.get_user_score(self.username)

    def add_point(self) -> int:
        self.actual_score += self.point_per_question
        return self.actual_score

    def victory(self) -> None:
        self.user_score = self.get_user_score(self.username)
        self.repository.save_score(self.username, self.user_score + self.actual_score)

    def game_over(self) -> None:

        self.user_score = self.get_user_score(self.username)
        self.repository.save_score(self.username, self.user_score - self.actual_score)

    def get_user_score(self, username: str) -> int:
        return self.repository.get_user_score(username)