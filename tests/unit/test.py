import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from game.question_node import QuestionNode

def _test_from_dict_node_class():
    question_node = QuestionNode("Does it bark?")
    
    data = {
    "value": "Does it have fur?",
        "yes": {"value": "Dog", "yes": None, "no": None},
        "no": {"value": "Bird", "yes": None, "no": None}
    }
    
    result = question_node.from_dict(data)
    
    assert [result.value, result.yes.value, result.no.value] == ["Does it have fur?", "Dog", "Bird"]
    print ("Function from_dict of the class QuestionNode is working")

def _test_to_dict_node_class():
    question_node = QuestionNode("Does it bark?")
    
    data = {
        "value": "Does it bark?",
        "yes": None,
        "no": None
    }
    
    assert question_node.to_dict() == data

    print ("Function to_dict of the class QuestionNode is working")

if __name__ == "__main__":
    _test_from_dict_node_class()
    _test_to_dict_node_class()