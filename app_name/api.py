from flask_restful import Api
from apispec import APISpec
from flask_apispec import FlaskApiSpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_jwt_extended import JWTManager


rest_api = Api(prefix="/api")


# jwt = JWTManager()
# jwt_key_scheme = {
#     "type": "apiKey", 
#     "in": "headers", 
#     "name": "Authorization"
# }


spec = APISpec(
    title="condopia API",
    version="v1",
    plugins=[MarshmallowPlugin(), ],
    openapi_version="2.0.0"
)
# spec.components.security_scheme("jwt", jwt_key_scheme)


docs = FlaskApiSpec()
