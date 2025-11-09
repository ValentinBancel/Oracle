from abc import ABC, abstractmethod


class IScoreRepository(ABC):


    @abstractmethod
    def user_exists(self, username: str) -> bool:
        pass

    @abstractmethod
    def create_user(self, username: str) -> None:
        pass

    @abstractmethod
    def get_user_score(self, username: str) -> int:
        pass

    @abstractmethod
    def save_score(self, username: str, score: int) -> None:
        pass