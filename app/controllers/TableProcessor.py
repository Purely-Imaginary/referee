def replace_names_with_teams(table):
    teams = {
        'Jacek Cieślak - Kamil Piorun': 'Sicarios z Secondigliano',
        'Paweł Pajchrowski - Wiktor Mazur': 'Czitory',
        'Amadeusz Opac - Dawid Markowski': 'Under Estimated',
        'Krzysztof Biernacki - Krzysztof Dziedzic': 'UX Team',
        'Aleksander Gacek - Jakub Bielecki': 'Chłopcy RODOrowcy',
        'Bartosz Janiak - Mateusz Bartosiak': 'Senegal',
        'Damian Zajkowski - Miłosz Dybizbański': 'Muminki',
        'Konrad Kozaczenko - Natalia Możejko': 'Kozaki',
        'Paweł Szablewski - Wojtek Dewódzki': 'Paweł i Wojciech',
        'Artur Radosz - Marcin Chmielnicki': 'CWKS Myszków',
    }

    replaced_scoreboard = []
    for team in table['scoreboard']:
        if team[0] in teams:
            replaced_scoreboard.append((teams[team[0]], team[1]))
        else:
            replaced_scoreboard.append((team[0], team[1]))

    replaced_detailed = {}
    for team_name, team_value in table['detailed'].items():
        if team_name in teams:
            key = teams[team_name]
        else:
            key = team_name

        inside_dict = {}
        for inside_key in team_value:
            if inside_key in teams:
                inside_replaced_key = teams[inside_key]
            else:
                inside_replaced_key = inside_key

            inside_dict[inside_replaced_key] = team_value[inside_key]

        replaced_detailed[key] = inside_dict

    return {'detailed': replaced_detailed, 'scoreboard': replaced_scoreboard}
