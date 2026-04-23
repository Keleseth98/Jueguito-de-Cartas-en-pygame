import json

class CardDatabase:
    def __init__(self, path):
        with open(path, "r") as f:
            data = json.load(f)

        self.cards = data["cards"]   
        self.decks = data["decks"]

    def get(self, card_id):
        return self.cards.get(card_id)