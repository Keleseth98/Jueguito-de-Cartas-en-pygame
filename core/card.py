class Card:
    def __init__(self, name):
        self.name = name

    def play(self, source, target, context):

        raise NotImplementedError("Cada carta debe implementar play()")