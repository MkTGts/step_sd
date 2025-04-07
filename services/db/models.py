from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Integer, String, Column, ForeignKey, TIMESTAMP


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    tg_id = Column(Integer)
    username = Column(String)
    fullname = Column(String)
    group_id = Column(Integer, ForeignKey("groups.group_id"))
    user_ip = Column(String)
    user_geo = Column(String)


class Group(Base):
    __tablename__ = "groups"

    group_id = Column(Integer, primary_key=True)
    group_name = Column(String)
    invite_token = Column(Integer)


class Ticket(Base):
    __tablename__ = "tickets"

    ticket_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id")),
    group_id = Column(Integer, ForeignKey("groups.group_id")),
    operator_id = Column(Integer, ForeignKey("users.user_id")),
    message = Column(String),
    status = Column(String),
    #priority = Column(String),
    created_at = Column(String),
    closed_at = Column(String)
    
