class Player:
    def __init__(self, id, name, present_rating=1000):
        self.present_rating = present_rating
        self.id = id
        self.name = name

    def change_rating(self, value, mongo_handler):
        # TODO: add coefficient which depends on number of matches x(4 - 0.5)?
        self.present_rating += value
        mongo_handler.db.players.update(
            {
                'name': self.name,
            },
            {
                "$inc":
                    {
                        'present_rating': value
                    }
            }
        )

    def insert_to_db(self, mongo_handler):
        mongo_handler.db.players.insert({
            "id": self.id,
            "name": self.name,
            "present_rating": self.present_rating,
            "wins": 0,
            "losses": 0,
        })
