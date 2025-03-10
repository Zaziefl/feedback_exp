class Item:
    def __init__(self, item_id, pr, nr, label, position):
        self.item_id = item_id
        self.pr = pr
        self.nr = nr
        self.label = label
        self.position = position
    pass


class RatingItem:
    def __init__(self, item_id, positive, text1, text2):
        self.item_id = item_id
        self.positive = positive
        self.text1 = text1
        self.text2 = text2
    pass


