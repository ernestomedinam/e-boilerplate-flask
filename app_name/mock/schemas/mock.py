from marshmallow import Schema, fields

from app_name.base.schemas.base import BaseSchema


class MockResponseSchema(BaseSchema):
    name = fields.String()
    parts = fields.Integer()
    description = fields.String()

class MockPatchSchema(Schema):
    parts = fields.Integer()
    description = fields.String()

class MockPostSchema(MockPatchSchema):
    name = fields.String(required=True)
    parts = fields.Integer(required=True)
