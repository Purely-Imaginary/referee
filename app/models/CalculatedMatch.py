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

        diff_coefficient = 400
        rating_change_coefficient = 1.5

        difference = (self.avg1elo - self.avg2elo) / diff_coefficient

        max_score = max(self.score1, self.score2)
        score_difference = self.score1 - self.score2

        estimation_for_team1 = 1 / (1 + pow(10, -difference))
        estimation_for_team2 = 1 / (1 + pow(10, difference))

        score_coefficient = max_score / max(estimation_for_team1, estimation_for_team2)

        self.estimated_score_for_team1 = estimation_for_team1 * score_coefficient
        self.estimated_score_for_team2 = estimation_for_team2 * score_coefficient
        estimated_score_difference = self.estimated_score_for_team1 - self.estimated_score_for_team2

        self.rating_change = rating_change_coefficient * (score_difference - estimated_score_difference)

    @staticmethod
    def calc_avg_elo(p1, p2):
        return (p1.present_rating + p2.present_rating) / 2
