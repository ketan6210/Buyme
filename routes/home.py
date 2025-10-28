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
from datetime import datetime

from .auth import login_required
from db import get_db
# from models.user import User

bp = Blueprint(
  "home",
  __name__,
)  # no prefix, so this blueprint will be used as the root (index)


@bp.route("/")
def index():
  return render_template("home/index.html")


@bp.route("/me")
@login_required
def profile():
  db = get_db()
  user_id = g.user["id"]
  # query for selling auctions
  selling_auctions = db.execute(
    """
        SELECT a.*, i.item_name, i.item_desc, c.category_name
        FROM auctions a
        JOIN item i ON a.item_id = i.item_id
        LEFT JOIN category c ON i.category_id = c.category_id
        WHERE a.user_id = ?
        ORDER BY a.auction_start DESC
    """,
    (user_id,),
  ).fetchall()

  # query for participating auctions
  participating_auctions = db.execute(
    """
        SELECT DISTINCT a.*, i.item_name, i.item_desc, c.category_name, 
               u.username as seller_username,
               MAX(b.bid_price) as your_highest_bid,
               b.bid_status
        FROM auctions a
        JOIN item i ON a.item_id = i.item_id
        LEFT JOIN category c ON i.category_id = c.category_id
        JOIN user u ON a.user_id = u.id
        JOIN bid b ON a.auction_id = b.auction_id
        WHERE b.user_id = ? AND a.user_id != ?
        GROUP BY a.auction_id
        ORDER BY a.auction_start DESC
    """,
    (user_id, user_id),
  ).fetchall()
  for value in participating_auctions[0]:
    print(value)

  # Get won auctions
  won_auctions = db.execute(
    """
      SELECT a.*, i.item_name, i.item_desc, c.category_name
      FROM auctions a
      JOIN item i ON a.item_id = i.item_id
      LEFT JOIN category c ON i.category_id = c.category_id
      JOIN bid b ON a.auction_id = b.auction_id
      WHERE b.user_id = ? AND b.bid_status = 'WON'
      ORDER BY a.auction_end DESC
  """,
    (user_id,),
  ).fetchall()

  # Calculate total spent
  total_spent_result = db.execute(
    """
      SELECT SUM(b.bid_price) as total_spent
      FROM bid b
      WHERE b.user_id = ? AND b.bid_status = 'WON'
  """,
    (user_id,),
  ).fetchone()

  total_spent = (
    total_spent_result["total_spent"] if total_spent_result["total_spent"] else 0
  )
  return render_template(
    "home/user_profile.html",
    selling_auctions=selling_auctions,
    participating_auctions=participating_auctions,
    won_auctions=won_auctions,
    total_spent=total_spent,
    now=datetime.now(),
  )
