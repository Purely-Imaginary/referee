class Player:
    def __init__(self, id, name, present_rating=1000):
        self.present_rating = present_rating
        self.id = id
        self.name = name
        self.matches = []
        self.progress = []
        self.skirmishes = {}

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
            "goals_scored": 0,
            "goals_lost": 0
        })

    @staticmethod
    def get_player_data(player_id, mongo_handler):
        player_data = mongo_handler.db.players.find_one({'id': int(player_id)})

        player_object = Player(int(player_id), player_data['name'], player_data['present_rating'])
        player_object.matches = player_object.get_all_matches(mongo_handler)
        player_object.calculate_progress()
        player_object.calculate_with_and_against()
        return player_object

    def calculate_with_and_against(self):
        self.skirmishes = {}
        data = {}
        friends = {}
        enemies = {}
        for match in self.matches:
            friend = match['team1']['player2']['name']
            opposing_team = match['team2']['player1']['name'] + " - " + match['team2']['player2']['name']
            if friend not in data:
                data[friend] = {}

            if opposing_team not in data[friend]:
                data[friend][opposing_team] = {'goals_scored': 0, 'goals_lost': 0}

            if friend not in friends:
                friends[friend] = 0

            if opposing_team not in enemies:
                enemies[opposing_team] = 0

            data[friend][opposing_team]['goals_scored'] += match['team1']['score']
            data[friend][opposing_team]['goals_lost'] += match['team2']['score']

            friends[friend] += match['team1']['score'] + match['team2']['score']
            enemies[opposing_team] += match['team1']['score'] + match['team2']['score']

        friends_sorted = [(k, friends[k]) for k in sorted(friends, key=friends.get, reverse=True)]
        enemies_sorted = [(k, enemies[k]) for k in sorted(enemies, key=enemies.get, reverse=True)]

        self.skirmishes = {'friends': friends_sorted, 'enemies': enemies_sorted, 'data': data}

    def calculate_progress(self):
        self.progress = []
        previous_match = False
        for match in self.matches:
            if not previous_match:
                previous_match = match
                continue

            if match['date'] == previous_match['date']:
                continue

            self.progress.append(
                {
                    'date': previous_match['date'],
                    'time': previous_match['time'],
                    'value': previous_match['team1']['player1']['present_rating'] + previous_match['team1'][
                        'rating_change'],
                    'match_id': previous_match['_id']
                }
            )
            previous_match = match

        self.progress.append(
            {
                'date': previous_match['date'],
                'time': previous_match['time'],
                'value': previous_match['team1']['player1']['present_rating'] + previous_match['team1'][
                    'rating_change'],
                'match_id': previous_match['_id']
            }
        )

    def get_all_matches(self, mongo_handler):
        data_team1 = mongo_handler.db.matches.find({
            "$or":
                [
                    {'team1.player1.id': self.id},
                    {'team1.player2.id': self.id}
                ]
        })
        matches = []
        for match in data_team1:
            if match['team1']['player1']['id'] != self.id:
                temp = match['team1']['player1']
                match['team1']['player1'] = match['team1']['player2']
                match['team1']['player2'] = temp

            matches.append(match)

        data_team2 = mongo_handler.db.matches.find({
            "$or":
                [
                    {'team2.player1.id': self.id},
                    {'team2.player2.id': self.id}
                ]
        })
        for match in data_team2:
            temp = match['team1']
            match['team1'] = match['team2']
            match['team2'] = temp
            if match['team1']['player1']['id'] != self.id:
                temp = match['team1']['player1']
                match['team1']['player1'] = match['team1']['player2']
                match['team1']['player2'] = temp

            matches.append(match)
        matches.sort(key=lambda d: d['date'] + d['time'])
        return matches
