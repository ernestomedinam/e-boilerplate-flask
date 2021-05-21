from marshmallow import Schema, fields


class MessageSchema(Schema):
    message = fields.String()

class BaseSchema(Schema):
    id = fields.Integer()
    created_at = fields.DateTime(format="iso")
    updated_at = fields.DateTime(format="iso")
