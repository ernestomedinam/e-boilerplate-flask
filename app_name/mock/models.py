import inspect
from app_name.db import db, ModelBase

# mock object class
class Mock(ModelBase):
    """
        a mock of some object for testing purposes.
            name: object name
            parts: how many parts this object has
            description: what it is
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    parts = db.Column(db.Integer, default=1, nullable=False)
    description = db.Column(db.Text())

    def __init__(self, validated_data):
        """
            assign validated data (valid keys, values and value types)
            arguments to mocked object. 
        """
        self.name = validated_data["name"]
        self.parts = validated_data["parts"]
        self.description = validated_data["description"]

    @classmethod
    def validate(self, input_data, create = False):
        """
            received input data is parsed to validated data
            dictionary, or rejected.
            create bool indicated validation for required
            creation input.
        """
        validated_data = {}
        have_required = True
        standard_mock = Mock({
            "name": "string",
            "parts": 1,
            "description": "string"
        })
        required_keys = ["name", "parts", "description"]
        for key in required_keys:
            if key in input_data:
                # check input_data[key] is same type as self.key prop
                if isinstance(input_data[key], type(getattr(standard_mock, key))):
                    attr = input_data.pop(key)
                    validated_data[key] = attr.strip() if isinstance(
                        attr, str
                    ) else attr
            else:
                have_required = False
        if len(validated_data) > 0:
            # some data is valid
            if (create and have_required) or not create:
                return validated_data
            else:
                return {
                    "status_code": 400,
                    "text": "sorry, can't create without required input."
                }
        else:
            return {
                "status_code": 400,
                "text": "Sorry, data is not valid."
            }
    
    @classmethod
    def create(self, input_data):
        """
            intermediary to init class instance and commit to db.
        """
        validated_data = self.validate(input_data, create = True)
        if "status_code" in validated_data:
            # data was not valid
            return validated_data # {status_code and text}
        else:
            mock_instance = Mock(validated_data)
            db.session.add(mock_instance)
            try:
                db.session.commit()
                return {
                    "status_code": 201,
                    "text": mock_instance.serialize()
                }
            except Exception as error:
                db.session.rollback()
                return {
                    "status_code": 500,
                    "text": error
                }

    def update(self, input_data):
        """
            intermediary to validate input data and commit updates to db.
        """
        validated_data = self.validate(input_data)
        if "status_code" in validated_data:
            return validated_data # {status_code and text}
        else:
            for key in validated_data:
                setattr(self, key, validated_data[key])
            try:
                db.session.commit()
                return {
                    "status_code": 200,
                    "text": self.serialize()
                }
            except Exception as error:
                db.session.rollback()
                return {
                    "status_code": 500,
                    "text": error
                }

    @classmethod
    def delete(self, instance_id):
        """
            delete self and commit to db.
        """
        mock_instance = Mock.query.filter_by(
            id=instance_id
        ).one_or_none()
        db.session.delete(mock_instance)
        try:
            db.session.commit()
            return {
                "status_code": 204,
                "text": "mock was deleted successfully."
            }
        except Exception as error:
            db.session.rollback()
            return {
                "status_code": 500,
                "text": error
            }

    def serialize(self):
        """
            return self as dictionary object
        """
        return {
            "id": self.id,
            "name": self.name,
            "parts": self.parts,
            "description": self.description
        }
