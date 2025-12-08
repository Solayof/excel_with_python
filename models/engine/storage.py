from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base import Base

class Dbstorage:
    __engine = None
    __session_factory = None

    @classmethod
    def init(cls):
        if cls.__engine:
            return

        cls.__engine = create_engine(
            "sqlite:///schooldb.db",
            connect_args={"check_same_thread": False, "timeout": 30},
            pool_pre_ping=True
        )

        with cls.__engine.connect() as conn:
            conn.exec_driver_sql("PRAGMA journal_mode=WAL;")

        Base.metadata.create_all(cls.__engine)

        cls.__session_factory = scoped_session(
            sessionmaker(
                bind=cls.__engine,
                autoflush=False,
                autocommit=False,
                expire_on_commit=False
            )
        )

        Base.query = cls.__session_factory.query_property()

    @classmethod
    def session(cls):
        """Always return the SAME scoped session"""
        if not cls.__session_factory:
            cls.init()
        return cls.__session_factory()

    @classmethod
    def new(cls, obj):
        cls.session().add(obj)

    @classmethod
    def save(cls):
        try:
            cls.session().commit()
        except Exception as e:
            cls.session().rollback()
            raise e

    @classmethod
    def delete(cls, obj=None):
        if obj:
            obj = cls.session().merge(obj)
            cls.session().delete(obj)

    @classmethod
    def close(cls):
        if cls.__session_factory:
            cls.__session_factory.remove()

    @classmethod
    def create_table(cls):
        """create models table in the database"""
        Base.metadata.create_all(cls.__engine)

    # @classmethod
    # def close(cls):
    #     """close storage"""
    #     if cls.__session:
    #         cls.__session.close()
    #         cls.__session = None
    #     if cls.__session_factory:
    #         cls.__session_factory.remove()
