import json
from typing import Optional, Tuple, Any, Dict
from game.question_node import QuestionNode


class Parsing(QuestionNode):
    def __init__(self, filename: str) -> None:
        self.filename: str = filename

    def save_json_tree(self, root: QuestionNode) -> None:
        with open(self.filename, "w") as f:
            json.dump(root.to_dict(), f, indent=2)
        print("Tree saved successfully.")

    def load_json_tree(
        self, default: Optional[QuestionNode] = None, verbose: bool = True
    ) -> Optional[QuestionNode]:
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                data: Dict[str, Any] = json.load(f)
        except Exception:
            if verbose:
                print(f"Error: unable to load/parse tree from '{self.filename}'")
            return default

        valid: bool
        valid, _ = self._validate_node_dict(data)
        if not valid:
            if verbose:
                print(f"Error: unable to load/parse tree from '{self.filename}'")
            return default

        try:
            root: Optional[QuestionNode] = self.from_dict(data)
            return root
        except Exception:
            if verbose:
                print(f"Error: unable to load/parse tree from '{self.filename}'")
            return default

    def _validate_node_dict(
        self, data: Any, path: str = "root"
    ) -> Tuple[bool, Optional[str]]:
        if data is None:
            return True, None

        if isinstance(data, str):
            return True, None

        if not isinstance(data, dict):
            return (
                False,
                f"expected dict or None or str at {path}, got {type(data).__name__}",
            )

        if "value" not in data:
            return False, f"missing 'value' key at {path}"
        if not isinstance(data["value"], str):
            return (
                False,
                f"'value' must be a string at {path}, got {type(data['value']).__name__}",
            )

        branch: str
        for branch in ("yes", "no"):
            if branch in data:
                ok: bool
                reason: Optional[str]
                ok, reason = self._validate_node_dict(
                    data[branch], path=f"{path}.{branch}"
                )
                if not ok:
                    return False, reason

        return True, None
