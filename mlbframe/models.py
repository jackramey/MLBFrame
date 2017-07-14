from mlbframe import db


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # ATTRIBUTES
    away_games_back = db.Column(db.Float)
    away_games_back_wc = db.Column(db.Float)
    away_loss = db.Column(db.Integer)
    away_team_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    away_win = db.Column(db.Integer)
    date = db.Column(db.Date)
    game_id = db.Column(db.String)
    game_number = db.Column(db.Integer)
    game_type = db.Column(db.String)
    gameday_id = db.Column(db.String)
    home_games_back = db.Column(db.Float)
    home_games_back_wc = db.Column(db.Float)
    home_loss = db.Column(db.Integer)
    home_team_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    home_win = db.Column(db.Integer)
    location = db.Column(db.String)
    scoreboard_id = db.Column(db.Integer, db.ForeignKey('scoreboard.id'))
    venue = db.Column(db.String)
    # RELATIONSHIPS
    away_team = db.relationship('Team', foreign_keys=[away_team_id])
    home_team = db.relationship('Team', foreign_keys=[home_team_id])
    scoreboard = db.relationship('Scoreboard', foreign_keys=[scoreboard_id])


class Inning(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # ATTRIBUTES
    away_runs = db.Column(db.Integer)
    home_runs = db.Column(db.Integer)
    inning_number = db.Column(db.Integer)


class Scoreboard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #ATTRIBUTES
    away_runs = db.Column(db.Integer)
    away_hits = db.Column(db.Integer)
    away_errs = db.Column(db.Integer)
    home_runs = db.Column(db.Integer)
    home_hits = db.Column(db.Integer)
    home_errs = db.Column(db.Integer)


class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # ATTRIBUTES
    abbrev = db.Column(db.String)
    city = db.Column(db.String)
    code = db.Column(db.String)
    division = db.Column(db.String)
    file_code = db.Column(db.String)
    league = db.Column(db.String)
    name = db.Column(db.String)


class TeamSeason(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # ATTRIBUTES
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    year = db.Column(db.Integer)
    # RELATIONSHIPS
    team = db.relationship('Team', foreign_keys=[team_id])


class Meta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # ATTRIBUTES
    last_updated = db.Column(db.Date)
