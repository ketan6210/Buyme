import functools

from flask import (
  Blueprint,
  flash,
  g,
  redirect,
  render_template,
  request,
  session,
  url_for,
)
from werkzeug.security import check_password_hash, generate_password_hash

from extensions import db
from models.user import User

bp = Blueprint("auth", __name__, url_prefix="/auth")


# store authentication related views here, as part of the /auth blueprint
@bp.route("/register", methods=("GET", "POST"))
def register():
  if request.method == "POST":
    f_name = request.form["f_name"]
    l_name = request.form["l_name"]
    username = request.form["username"]
    password = request.form["password"]
    # TODO: need first name, last name
    error = None

    if not username:
      error = "Username is required."
    elif not password:
      error = "Password is required."
    elif not f_name:
      error = "First Name is required."
    elif not l_name:
      error = "Last Name is required."

    if error is None:
      try:
        new_user = User(
          username=username,
          password=generate_password_hash(password),
          user_type="customer",
          f_name=f_name,
          l_name=l_name,
        )
        db.session.add(new_user)
        db.session.commit()
      except Exception as e:
        db.session.rollback()
        error = f"User {username} is already registered."
      else:
        return redirect(url_for("auth.login"))
        # redirect to login view

    flash(error)

  return render_template("auth/register.html")


@bp.route("/login", methods=("GET", "POST"))
def login():
  if request.method == "POST":
    username = request.form["username"]
    password = request.form["password"]
    # db = get_db()
    error = None
    user = User.query.filter_by(username=username).first()

    if user is None:
      error = "Incorrect username."
    elif not check_password_hash(user.password, password):
      error = "Incorrect password."

    if error is None:
      # store the userID as a new session. for subsequent requests from this user, load their information
      session.clear()
      session["user_id"] = user.user_id  # pyright: ignore[reportOptionalMemberAccess]
      return redirect(url_for("index"))

    flash(error)

  return render_template("auth/login.html")


# this function will be run before all view functions. It stores the user information in g.user which lasts for the entire request.
@bp.before_app_request
def load_logged_in_user():
  user_id = session.get("user_id")

  if user_id is None:
    g.user = None
  else:
    g.user = User.query.filter_by(user_id=user_id).first()


# clear the session, so that load_logged_in_user won't load the user for subsequent requests
@bp.route("/logout")
def logout():
  session.clear()
  return redirect(url_for("index"))


# takes a view and returns a wrapped version of it that redirects to the login page if the user is not logged in
# userful for requests that require login, like writing blog posts.
# now any view tagged with @login_required will be wrapped with wrapped_view (checks login)
def login_required(view):
  @functools.wraps(view)
  def wrapped_view(**kwargs):
    if g.user is None:
      return redirect(url_for("auth.login"))

    return view(**kwargs)  # return original view

  return wrapped_view
