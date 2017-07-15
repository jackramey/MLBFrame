import sys

activate_this = '/var/www/mlbframe/venv/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

sys.path.append('/var/www/mlbframe')
from mlbframe import app as application