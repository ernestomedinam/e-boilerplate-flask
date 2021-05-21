import enum
import json
from datetime import timezone

from app_name.db import db


class BaseEnum(enum.Enum):
    """ base class for Enum classes """

    @classmethod
    def list_values(cls):
        return list(map(lambda item: item.value, cls))

    @classmethod
    def list_names(cls):
        return list(map(lambda item: item.name, cls))

    @classmethod
    def serialize(cls):
        return json.dumps(dict(list(map(lambda item: (item.name, item.value), cls))))


class BaseModel(db.Model):
    __abstract__ = True
    __table_args__ = {
        "mysql_engine": "InnoDB"
    }
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime(timezone=True), default=db.func.now(), nullable=False)
    updated_at = db.Column(db.DateTime(timezone=True), default=db.func.now(), onupdate=db.func.now(), nullable=False)

    def __init__(self, **validated_data):
        """ class constructor """
        self._provision(validated_data)

    def _provision(self, data):
        """ sets attributes for keys in validated_data """
        count = 0
        for (key, value) in {**data}.items():
            if hasattr(self, key):
                count += 1
                setattr(self, key, data.pop(key))
        return count > 0

    @classmethod
    def create(cls, **validated_data):
        """ runs class constructor, commits to db and returns instance """
        instance = cls(**validated_data)
        if isinstance(instance, cls):
            db.session.add(instance)
            try:
                db.session.commit()
                return instance
            except Exception as error:
                db.session.rollback()
                print(error.args)
        return None

    def update(self, **validated_data):
        """ updates attributes for self from keys on validated_data, commits to db and returns boolean """
        updated = self._provision(validated_data)
        if updated:
            try:
                db.session.commit()
                return True
            except Exception as error:
                db.session.rollback()
                print(error.args)
        return False

    def delete(self):
        """ deletes and commits to db, returns boolean """
        db.session.delete(self)
        try:
            db.session.commit()
            return True
        except Exception as error:
            db.session.rollback()
            print(error.args)
        return False

    @classmethod
    def get(cls, **kwargs):
        """ queries class for a specific criteria with unique value; expects/returns one or none """
        # kwergs = map(lambda key, value: f"{key}={value}", kwargs.items())
        return cls.query.filter_by(
            **kwargs
        ).one_or_none()

    @classmethod
    def find(cls, **filters):
        """ queries class for named arguments as filters """
        return cls.query.filter_by(**filters).all()

    @classmethod
    def all(cls):
        return cls.query.all()
