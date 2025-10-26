from sqlalchemy import (
  Integer,
  String,
  Column,
  Text,
  Enum,
  ForeignKey,
  DECIMAL,
  DateTime,
  BigInteger,
)
from sqlalchemy.orm import Mapped, relationship
from extensions import db


class User(db.Model):
  __tablename__ = "users"

  user_id = Column(Integer, primary_key=True, autoincrement=True)
  username = Column(String(50), unique=True, nullable=False)
  password = Column(String(255), nullable=False)
  f_name = Column(String(50))
  l_name = Column(String(50))
  user_type = Column(Enum("customer", "representative", "admin"), nullable=False)

  # Relationships
  # auctions = relationship(
  #   "Auction", back_populates="user", cascade="all, delete-orphan"
  # )
  # bids = relationship("Bid", back_populates="user", cascade="all, delete-orphan")

  def __init__(
    self, username=None, password=None, user_type="customer", f_name=None, l_name=None
  ):
    self.username = username
    self.password = password
    self.user_type = user_type
    self.f_name = f_name
    self.l_name = l_name

  def __repr__(self):
    return f"<User(username={self.username}, type={self.user_type})>"
