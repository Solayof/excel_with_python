#!/usr/bin/python3
from datetime  import datetime, date, timezone
from sqlalchemy import Column, DateTime, func, String
from uuid import uuid4
import models


class BaseModel():
    id = Column(String(36), primary_key=True, default= lambda: str(uuid4()))
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc))

    def __init__(self, *args, **kwargs):
        """initialize user  base model"""
        if kwargs:
            for key, value in kwargs.items():
                da = ["dob", "pub_date", "date_transfer", "last_promote_date"]
                if key in ["created_at", "updated_at"]:
                    continue
                if key in da and isinstance(value, str):
                  try:
                    value = date.fromisoformat(value)
                  except ValueError:
                    continue
                if key in da:
                    if isinstance(value, datetime) is False:
                        continue
                setattr(self, key, value)
            self.created_at = datetime.now()
            self.updated_at = self.created_at

        if self.id is None:
            self.id = str(uuid4())
    
    def __str__(self):
        """string representation

        Returns:
            _type_: string
        """
        return f"<{self.__class__.__name__}> <{self.id}> {self.__dict__}"
        
    def __repr__(self):
        """string representation

        Returns:
            _type_: string
        """
        return f"{self.id}"
    
    def save(self):
        """save the object instance
        """
        self.updated_at = datetime.now(timezone.utc)
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """dictionary representation of class instance

        Returns:
            _type_: dict
        """        
        new_dict = self.__dict__.copy()
        new_dict.pop("_sa_instance_state", None)
        new_dict.pop("_password", None)
        new_dict["created_at"] = self.created_at.isoformat()
        new_dict["updated_at"] = self.updated_at.isoformat()
        return new_dict

    def delete(self):
        """delete object instance
        """        
        models.storage.delete(self)
        models.storage.save()

    @classmethod
    def all(cls):
        objs = {}
        for obj in cls.query.all():
            objs[obj.id] = obj.to_dict()
        return objs

    @classmethod
    def get(cls, id=None):
        """get instance of a class by its primary key

        Args:
            id (class primarykey type, optional):
            the primary key of class to get. Defaults to None.

        Returns:
            _type_: class instance if exists, None otherwise
        """
        if id is None:
            return id
        return cls.query.session.get(cls, id)
    @classmethod
    def paginate(cls, page=1, per_page=10):
        """paginate the query

        Args:
            page (int, optional): page to get. Defaults to 1.
            per_page (int, optional): number per page. Defaults to 10.

        Returns:
            tuple: (count, queryset, next_page)
        """        
        offset = per_page * (page - 1)
        count = cls.query.with_entities(func.count(cls.id)).scalar()
        query = cls.query.offset(offset).limit(per_page)
        next_page = page + 1 if page * per_page < count else 1
        return count, query, next_page
