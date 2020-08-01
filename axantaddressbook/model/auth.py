# -*- coding: utf-8 -*-
from sqlalchemy.orm import mapper, relation
from sqlalchemy import Column
from sqlalchemy.types import Integer, Unicode
from axantaddressbook.model import DeclarativeBase, metadata, DBSession

class User(DeclarativeBase):
    __tablename__ = 'tg_user'

    user_id = Column(Integer, autoincrement=True, primary_key=True)
    user_name = Column(Unicode(16), unique=True, nullable=False)
    email_address = Column(Unicode(255), unique=True, nullable=False)
    display_name = Column(Unicode(255))
    password = Column(Unicode(255), nullable=False)

class Permission(DeclarativeBase):
    __tablename__ = 'tg_permission'

    permission_id = Column(Integer, autoincrement=True, primary_key=True)
    permission_name = Column(Unicode(20), unique=True, nullable=False)
    description = Column(Unicode(255))