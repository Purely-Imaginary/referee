import copy


class CalculatedMatch:
    def __init__(self, date, time, player11, player12, player21, player22, score1, score2, league):
        self.date = date
        self.time = time
        self.player11 = copy.deepcopy(player11)
        self.player12 = copy.deepcopy(player12)
        self.player21 = copy.deepcopy(player21)
        self.player22 = copy.deepcopy(player22)
        self.score1 = score1
        self.score2 = score2
        self.league = league
        self.avg1elo = CalculatedMatch.calc_avg_elo(player11, player12)
        self.avg2elo = CalculatedMatch.calc_avg_elo(player21, player22)

        diff_coefficient = 800
        rating_change_coefficient = 40

        difference = (self.avg1elo - self.avg2elo) / diff_coefficient

        max_score = max(self.score1, self.score2)
        score_difference = self.score1 - self.score2

        estimation_for_team1 = 1 / (1 + pow(10, -difference))
        estimation_for_team2 = 1 / (1 + pow(10, difference))

        score_coefficient = max_score / max(estimation_for_team1, estimation_for_team2)

        self.estimated_score_for_team1 = estimation_for_team1 * score_coefficient
        self.estimated_score_for_team2 = estimation_for_team2 * score_coefficient
        estimated_score_difference = self.estimated_score_for_team1 - self.estimated_score_for_team2

        self.rating_change = rating_change_coefficient / 20 * (score_difference - estimated_score_difference)

    @staticmethod
    def calc_avg_elo(p1, p2):
        return (p1.present_rating + p2.present_rating) / 2

    def insert_to_db(self, mongo_handler):
        mongo_handler.db.matches.insert({
            "team1": {
                "player1": {
                    "id": self.player11.id,
                    "name": self.player11.name,
                    "present_rating": self.player11.present_rating,
                },
                "player2": {
                    "id": self.player12.id,
                    "name": self.player12.name,
                    "present_rating": self.player12.present_rating,
                },
                "score": self.score1,
                "estimated_score": self.estimated_score_for_team1,
                "rating_change": self.rating_change,
            },
            "team2": {
                "player1": {
                    "id": self.player21.id,
                    "name": self.player21.name,
                    "present_rating": self.player21.present_rating,
                },
                "player2": {
                    "id": self.player22.id,
                    "name": self.player22.name,
                    "present_rating": self.player22.present_rating,
                },
                "score": self.score2,
                "estimated_score": self.estimated_score_for_team2,
                "rating_change": -self.rating_change,
            },
            "date": self.date,
            "time": self.time,
            "league": self.league
        })

    def update_players(self, mongo_handler):
        # wins and losses only

        if self.score1 > self.score2:
            mongo_handler.db.players.update_many(
                {
                    "$or": [
                        {'name': self.player11.name},
                        {'name': self.player12.name}
                    ]
                },
                {"$inc": {'wins': 1}}
            )

            mongo_handler.db.players.update_many(
                {
                    "$or": [
                        {'name': self.player21.name},
                        {'name': self.player22.name}
                    ]
                },
                {"$inc": {'losses': 1}}
            )
        elif self.score1 < self.score2:
            mongo_handler.db.players.update_many(
                {
                    "$or": [
                        {'name': self.player11.name},
                        {'name': self.player12.name}
                    ]
                },
                {"$inc": {'losses': 1}}
            )

            mongo_handler.db.players.update_many(
                {
                    "$or": [
                        {'name': self.player21.name},
                        {'name': self.player22.name}
                    ]
                },
                {"$inc": {'wins': 1}}
            )
