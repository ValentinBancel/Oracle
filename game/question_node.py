from typing import Optional, Dict, Any


class QuestionNode:
    def __init__(
        self,
        value: str,
        yes: Optional["QuestionNode"] = None,
        no: Optional["QuestionNode"] = None,
    ) -> None:
        self.value: str = value  # The question or final answer
        self.yes: Optional["QuestionNode"] = yes  # Node if answer is "Yes"
        self.no: Optional["QuestionNode"] = no  # Node if answer is "No"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "value": self.value,
            "yes": self.yes.to_dict() if self.yes else None,
            "no": self.no.to_dict() if self.no else None,
        }

    def from_dict(self, data: Optional[Dict[str, Any]]) -> Optional["QuestionNode"]:
        if data is None:
            return None
        node: QuestionNode = QuestionNode(data["value"])
        node.yes = self.from_dict(data["yes"])
        node.no = self.from_dict(data["no"])
        return node
