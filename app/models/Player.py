class Player:
    def __init__(self, id, name, present_rating=1000):
        self.present_rating = present_rating
        self.id = id
        self.name = name

    def change_rating(self, value):
        # TODO: add coefficient which depends on number of matches x(4 - 0.5)?
        self.present_rating += value
