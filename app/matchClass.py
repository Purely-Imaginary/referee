class match:
    def __init__(self, date, time, player11, player12, player21, player22, score1, score2, league):
        self.date = date
        self.time = time
        self.player11 = player11
        self.player12 = player12
        self.player21 = player21
        self.player22 = player22
        self.score1 = score1
        self.score2 = score2
        self.league = league

    def calculate(self, p11elo, p12elo, p21elo, p22elo):
        diffCoefficient = 400
        ratingChangeCoefficient = 5

        avg1elo = (p11elo+p12elo) / 2
        avg2elo = (p21elo+p22elo) / 2
        difference = (avg1elo - avg2elo) / diffCoefficient

        maxScore = max(self.score1, self.score2)
        scoreDifference = self.score1 - self.score2

        estimationForTeam1 = 1/(1+pow(10, -difference))
        estimationForTeam2 = 1/(1+pow(10, difference))

        scoreCoefficient = maxScore / max(estimationForTeam1, estimationForTeam2)

        estimatedScoreForTeam1 = estimationForTeam1 * scoreCoefficient
        estimatedScoreForTeam2 = estimationForTeam2 * scoreCoefficient
        estimatedScoreDifference = estimatedScoreForTeam1 - estimatedScoreForTeam2

        ratingChange = ratingChangeCoefficient*(scoreDifference - estimatedScoreDifference)

        calculatedMatch = {
            'match': self,
            'avg1elo': avg1elo,
            'estimatedScore': str(estimatedScoreForTeam1) + ":" + str(estimatedScoreForTeam2),
            'avg2elo': avg2elo,
            'ratingChange': ratingChange
        }
        return calculatedMatch
