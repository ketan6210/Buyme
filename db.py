import sqlite3
from datetime import datetime

import click
from flask import current_app, g
# g that lasts for an entire request. It is a special object that stores data about the current db connection.
# if get_db is called again by the same request it will be reused from g
# current_app is refernce to the app that made the request


def get_db():
  if "db" not in g:
    g.db = sqlite3.connect(
      current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
    )
    g.db.row_factory = sqlite3.Row
    # tells the connection to return rows like dicts.

  return g.db


def close_db(e=None):
  db = g.pop("db", None)

  if db is not None:
    db.close()


def init_db():
  db = get_db()

  with current_app.open_resource("schema.sql") as f:
    db.executescript(f.read().decode("utf8"))


@click.command("init-db")
def init_db_command():
  """Clear the existing data and create new tables."""
  init_db()
  click.echo("Initialized the database.")


sqlite3.register_converter("timestamp", lambda v: datetime.fromisoformat(v.decode()))


def init_app(app):
  # registers close_db with the app instance AND adds the init-db CLI command
  app.teardown_appcontext(close_db)
  app.cli.add_command(init_db_command)
