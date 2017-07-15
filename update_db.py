import datetime

from mlbframe import app, db
from mlbframe.mlb_api import get_master_scoreboard
import mlbframe.models as models


def process_master_scoreboard(year, month, day):
    data = get_master_scoreboard(year, month, day)
    if data is None:
        return
    gameday_data = data.get('data')
    if not gameday_data:
        return
    gameday_games = gameday_data.get('games')
    if not gameday_games:
        return
    gameday_game = gameday_games.get('game')
    if not gameday_game or not type(gameday_game) is list:
        return
    for game in gameday_game:
        g = models.Game()
        g.away_games_back = 0 if not is_float(game['away_games_back']) else float(game['away_games_back'])
        g.away_games_back_wc = 0 if not is_float(game['away_games_back_wildcard']) else float(game['away_games_back_wildcard'])
        g.away_loss = int(game['away_loss'])
        g.away_win = game['away_win']
        g.date = datetime.date(year, month, day)
        g.game_id = game['id']
        g.game_number = game['game_nbr']
        g.game_type = game['game_type']
        g.gameday_id = game['gameday']
        g.home_games_back = 0 if not is_float(game['home_games_back']) else float(game['home_games_back'])
        g.home_games_back_wc = 0 if not is_float(game['home_games_back_wildcard']) else float(game['home_games_back_wildcard'])
        g.home_loss = game['home_loss']
        g.home_win = game['home_win']
        g.location = game['location']
        g.venue = game['venue']
        # Set up teams
        away_team = models.Team.query.filter_by(abbrev=game['away_name_abbrev']).first()
        if away_team is None:
            away_team = models.Team()
            away_team.abbrev = game['away_name_abbrev']
            away_team.city = game['away_team_city']
            away_team.code = game['away_code']
            away_team.division = game['away_division']
            away_team.file_code = game['away_file_code']
            away_team.league = "NL" if game['away_league_id'] == "104" else "AL"
            away_team.name = game['away_team_name']
        home_team = models.Team.query.filter_by(abbrev=game['home_name_abbrev']).first()
        if home_team is None:
            home_team = models.Team()
            home_team.abbrev = game['home_name_abbrev']
            home_team.city = game['home_team_city']
            home_team.code = game['home_code']
            home_team.division = game['home_division']
            home_team.file_code = game['home_file_code']
            home_team.league = "NL" if game['home_league_id'] == "104" else "AL"
            home_team.name = game['home_team_name']
        db.session.add(away_team)
        db.session.add(home_team)
        g.away_team = away_team
        g.home_team = home_team
        # Set up scoreboard
        sb = models.Scoreboard()
        linescore = game.get('linescore')
        if linescore:
            sb.away_hits = int(linescore['h']['away'])
            sb.away_runs = int(linescore['r']['away'])
            sb.away_errs = int(linescore['e']['away'])
            sb.home_hits = int(linescore['h']['home'])
            sb.home_runs = int(linescore['r']['home'])
            sb.home_errs = int(linescore['e']['home'])
            g.scoreboard = sb
            db.session.add(sb)
        db.session.add(g)
        db.session.commit()


def is_float(value):
    return not (value == '' or value == '-')


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + datetime.timedelta(n)


if __name__ == '__main__':
    start_date = datetime.date(2017, 4, 1)
    end_date = datetime.date.today()
    for single_date in daterange(start_date, end_date):
        process_master_scoreboard(single_date.year, single_date.month, single_date.day)
