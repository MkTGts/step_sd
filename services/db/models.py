from sqlalchemy import Integer, String, Column, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
#from services.db.database import Base


Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)
    tg_id = Column(Integer)
    username = Column(String)
    fullname = Column(String)
    #user_type = Column(Integer)  # 1 - admins, 2 - operators, 3 - users
    group_id = Column(Integer, ForeignKey("groups.group_id"))
    user_ip = Column(String)
    user_geo = Column(String)


class Operator(Base):
    __tablename__ = "operators"

    operator_id = Column(Integer, primary_key=True)
    tg_id = Column(Integer)
    username = Column(String)
    fullname = Column(String)
    group_id = Column(Integer, ForeignKey("groups.group_id"))


class Admin(Base):
    __tablename__ = "admins"

    admin_id = Column(Integer, primary_key=True)
    tg_id = Column(Integer)
    username = Column(String)
    fullname = Column(String)
    


class Group(Base):
    __tablename__ = "groups"

    group_id = Column(Integer, primary_key=True)
    group_name = Column(String)
    invite_token = Column(Integer)



class Ticket(Base):
    __tablename__ = "tickets"

    ticket_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    group_id = Column(Integer, ForeignKey("groups.group_id"))
    operator_id = Column(Integer, ForeignKey("operators.operator_id"))
    message = Column(String)
    status = Column(String)
    created_at = Column(String)
    closed_at = Column(String)
    
