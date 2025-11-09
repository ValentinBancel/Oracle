import pandas as pd
from interfaces.i_score_repository import IScoreRepository


class CSVScoreRepository(IScoreRepository):

    def __init__(self, filename: str = './scoring.csv') -> None:

        self.filename: str = filename
        self._ensure_file_exists()

    def _ensure_file_exists(self) -> None:

        try:
            with open(self.filename, 'r') as f:
                pass
        except FileNotFoundError:
            self._create_file()

    def _create_file(self) -> None:

        df = pd.DataFrame(columns=['username', 'last_score', 'score_total'])
        df.to_csv(self.filename, index=False)

    def user_exists(self, username: str) -> bool:

        try:
            df = pd.read_csv(self.filename)
            df = df.set_index('username')
            return username in df.index
        except Exception:
            # If there's an error, try to create the user
            try:
                self.create_user(username)
                return True
            except Exception:
                return False

    def create_user(self, username: str) -> None:

        try:
            df = pd.read_csv(self.filename)
            new_user = [{
                'username': username,
                'last_score': 0,
                'score_total': 0
            }]
            df = pd.concat([df, pd.DataFrame(new_user)], ignore_index=False)
            df.to_csv(self.filename, index=False)
        except Exception as e:
            print(f"Error creating user: {e}")

    def get_user_score(self, username: str) -> int:

        try:
            df = pd.read_csv(self.filename)
            user_entries = df[df['username'] == username]
            if not user_entries.empty:
                return int(user_entries.iloc[-1]['score_total'])
            else:
                self.create_user(username)
                return 0
        except Exception:
            self.create_user(username)
            return 0

    def save_score(self, username: str, score: int) -> None:

        try:
            df = pd.read_csv(self.filename)

            # Create a new entry for this game
            new_entry = {
                'username': username,
                'last_score': score,
                'score_total': score
            }

            # Add the new entry to the dataframe
            df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)

            # Save back to CSV
            df.to_csv(self.filename, index=False)
        except Exception as e:
            print(f"Error saving score: {e}")

    def read_file(self) -> pd.DataFrame:
        return pd.read_csv(self.filename)