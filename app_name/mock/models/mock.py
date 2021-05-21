import inspect

from app_name.db import db
from app_name.base.models.base import BaseModel


# mock object class
class Mock(BaseModel):
    """
        a mock of some object for testing purposes.
            name: object name
            parts: how many parts this object has
            description: what it is
    """
    name = db.Column(db.String(80), nullable=False, unique=True)
    parts = db.Column(db.Integer, default=1, nullable=False)
    description = db.Column(db.String(250))

    @classmethod
    def validate(cls, input_data, create=False):
        """
            received input data is parsed to validated data
            dictionary, or rejected.
            create bool indicated validation for required
            creation inputs.
        """
        validated_data = {**input_data}
        return validated_data
    
    @classmethod
    def create(cls, **kwargs):
        """
            intermediary to init class instance and commit to db.
        """
        validated_data = cls.validate(kwargs, create=True)
        if validated_data is None:
            return None
        return super().create(**validated_data)

    def update(self, **kwargs):
        """
            intermediary to validate input data and commit updates to db.
        """
        validated_data = self.validate(kwargs)
        if validated_data is None:
            return None # {status_code and text}
        return super().update(**validated_data)
