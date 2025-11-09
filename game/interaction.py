from typing import Literal


class Interaction:
    def __init__(self) -> None:
        pass

    def requestInput(self, message: str, input_type: Literal["bool", "str"]) -> str:
        response: str = input(message)

        match input_type:

            case "bool":
                if response.lower() == "true" or response.lower() == "false":
                    return response.lower()
                else:
                    print("Please answer true or false.")
                    return self.requestInput(message, "bool")

            case "str":
                if isinstance(response, str):
                    return response
                else:
                    print("Please enter text in this field")
                    return self.requestInput(message, "text")
