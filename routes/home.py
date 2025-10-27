# define / route
from flask import (
  Blueprint,
  flash,
  g,
  redirect,
  render_template,
  request,
  url_for,
)
from werkzeug.exceptions import abort

from .auth import login_required
import db
# from models.user import User

bp = Blueprint(
  "home",
  __name__,
)  # no prefix, so this blueprint will be used as the root (index)


@bp.route("/")
def index():
  return render_template("home/index.html")
