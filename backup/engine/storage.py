#!/usr/bin/python3
"""storage engine"""
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base import Base


class Dbstorage():
    """connecting database"""
    __engine = None
    __session = None
    tables = {}

    @classmethod
    def init(cls):
        """initialzed the db engine"""
        username = "school_admin"
        password = "arisekola"
        hostname = "localhost"
        database = getenv("DATABASE", "school_db")

        if not cls.__engine or not cls.__session:
            cls.__engine = create_engine(
                 "sqlite:///db/schooldb.db", #f"mysql+mysqldb://{username}:{password}@{hostname}/{database}",
                 connect_args={"check_same_thread": False}, # for sqlite
                pool_pre_ping=True
            )
            Base.metadata.create_all(cls.__engine)
            cls.__session = scoped_session (
                sessionmaker(bind=cls.__engine, expire_on_commit=False)
            )
            Base.query = cls.__session.query_property()
    
    @classmethod
    def open_session(cls):
        """open new session"""
        if not cls.__session:
            cls.init()
    
    @classmethod
    def new(cls, obj):
        """add newobj to current db session"""
        cls.__session.add(obj)
    
    @classmethod
    def save(cls):
        """save object instance
        """        
        cls.__session.commit()
    
    @classmethod
    def delete(cls, obj=None):
        """delete obj instance

        Args:
            obj (class, optional): object to delete. Defaults to None.
        """        
        cls.__session.delete(obj)
    
    @classmethod
    def create_table(cls):
        """create models table in the database
        """        
        Base.metadata.create_all(cls.__engine)

    @classmethod
    def close(cls):
        """close storage
        """        
        if cls.__session:
            cls.__session.remove()
