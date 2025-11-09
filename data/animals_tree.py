import json

class AnimalNode:
    def __init__(self, value, yes=None, no=None):
        self.value = value
        self.yes = yes
        self.no = no


class AnimalTree:
    def __init__(self):
        # ROOT - Build initial tree (modern domestic animals example)
        self.root = AnimalNode("Does it live mostly on land?")

        # MAIN BRANCHES
        self.root.yes = AnimalNode("Does it have fur or hair?")
        self.root.no = AnimalNode("Does it live mainly in water?")

        # ---------------- YES BRANCH (Land animals)
        self.root.yes.yes = AnimalNode("Is it a household companion?")
        self.root.yes.no = AnimalNode("Does it have feathers?")

        # Household companions
        self.root.yes.yes.yes = AnimalNode("Is it loyal and social?")
        self.root.yes.yes.no = AnimalNode("Is it small and usually kept in cages?")

        # Dogs, cats, ferrets
        self.root.yes.yes.yes.yes = AnimalNode("Dog")
        self.root.yes.yes.yes.no = AnimalNode("Cat")

        # Small caged mammals
        self.root.yes.yes.no.yes = AnimalNode("Hamster")
        self.root.yes.yes.no.no = AnimalNode("Rabbit")

        # Feathers branch (birds)
        self.root.yes.no.yes = AnimalNode("Is it colorful or can mimic sounds?")
        self.root.yes.no.no = AnimalNode("Is it raised for food or eggs?")

        self.root.yes.no.yes.yes = AnimalNode("Parrot")
        self.root.yes.no.yes.no = AnimalNode("Canary")
        self.root.yes.no.no.yes = AnimalNode("Chicken")
        self.root.yes.no.no.no = AnimalNode("Duck")

        # ---------------- NO BRANCH (Non-furry animals)
        self.root.no.yes = AnimalNode("Does it have fins?")
        self.root.no.no = AnimalNode("Does it have scales or a shell?")

        # Aquatic animals
        self.root.no.yes.yes = AnimalNode("Is it colorful and small?")
        self.root.no.yes.no = AnimalNode("Is it slow-moving?")
        self.root.no.yes.yes.yes = AnimalNode("Goldfish")
        self.root.no.yes.yes.no = AnimalNode("Koi Carp")
        self.root.no.yes.no.yes = AnimalNode("Turtle")
        self.root.no.yes.no.no = AnimalNode("Frog")

        # Reptiles and others
        self.root.no.no.yes = AnimalNode("Does it have legs?")
        self.root.no.no.no = AnimalNode("Is it an insect?")

        # Reptiles
        self.root.no.no.yes.yes = AnimalNode("Can it change color?")
        self.root.no.no.yes.no = AnimalNode("Moves by slithering?")

        self.root.no.no.yes.yes.yes = AnimalNode("Chameleon")
        self.root.no.no.yes.yes.no = AnimalNode("Lizard")

        self.root.no.no.yes.no.yes = AnimalNode("Snake")
        self.root.no.no.yes.no.no = AnimalNode("Tortoise")

        # Insects
        self.root.no.no.no.yes = AnimalNode("Has colorful wings?")
        self.root.no.no.no.no = AnimalNode("Has many legs?")

        self.root.no.no.no.yes.yes = AnimalNode("Butterfly")
        self.root.no.no.no.yes.no = AnimalNode("Bee")
        self.root.no.no.no.no.yes = AnimalNode("Spider")
        self.root.no.no.no.no.no = AnimalNode("Ant")


def _node_to_dict(node):
    if node is None:
        return None
    return {
        "value": node.value,
        "yes": _node_to_dict(node.yes),
        "no": _node_to_dict(node.no)
    }


if __name__ == "__main__":
    tree = AnimalTree()
    tree_dict = _node_to_dict(tree.root)

    with open("animals_tree.json", "w", encoding="utf-8") as f:
        json.dump(tree_dict, f, indent=4, ensure_ascii=False)

    print("✅ JSON successfully generated: animals_tree.json")
