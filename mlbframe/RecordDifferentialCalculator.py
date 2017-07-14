import datetime

from sqlalchemy import and_, or_, extract

from mlbframe.models import Game, Team


def calculate(team_abbrev, year=None):
    if year is None:
        year = datetime.date.today().year
    differentials = []
    team_id = Team.query.filter(Team.abbrev == team_abbrev).first().id
    games = Game.query.filter(and_(and_(or_(
        Game.away_team_id == team_id,
        Game.home_team_id == team_id),
        Game.game_type == 'R'),
        extract('year', Game.date) == year)
    ).order_by(Game.id)
    for game in games:
        # Pseudocode for dealing with days off
        # Things to decide before implementing this: Do we want to account for date equality or number of games played?
        # How does this work for double headers? Might become a shitty graph in that case.
        # days_between_games = game.date - prev_game.date
        # if days_between_games > 1:
        #  differentials.append(differentials[-1])
        if game.away_team_id == team_id:
            differentials.append(game.away_win - game.away_loss)
        else:
            differentials.append(game.home_win - game.home_loss)
    return differentials


