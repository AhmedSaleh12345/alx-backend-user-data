#!/usr/bin/env python3
"""db module"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from typing import Dict

from user import Base, User


class DB:
    """db class"""

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db")
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        should save the user to the database.
        No validations are required at this stage.
        """
        session = self._session
        try:
            new_user = User(email=email, hashed_password=hashed_password)
            session.add(new_user)
            session.commit()
        except Exception:
            session.rollback()
            new_user = None
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """
        Find user
        """
        sesssion = self._session
        if not kwargs:
            raise InvalidRequestError
        quary = sesssion.query(User).filter_by(**kwargs).one()
        if quary:
            return quary
        else:
            raise NoResultFound
