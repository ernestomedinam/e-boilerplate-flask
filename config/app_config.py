# scenario based config overrides, including env variables
import os
from flask_dotenv import DotEnv

class BaseConfig(object):
    ENV = "development"
    DEBUG = True

    @classmethod
    def init_app(self, app):
        env = DotEnv()
        path = os.getcwd().replace("config", "")
        env.init_app(app, env_file=os.path.join(path, ".env"), verbose_mode=True)

        # update database uri
        prefix = self.__name__.replace("Config", "").upper()
        env.alias(maps={
            prefix + "_CONNECTION_STRING": "SQLALCHEMY_DATABASE_URI"
        })

class DevelopmentConfig(BaseConfig):
    MY_DEV_VARIABLE = "Cojones!"
    DEVELOPMENT_CONNECTION_STRING = os.environ.get("DEVELOPMENT_CONNECTION_STRING")

class TestConfig(BaseConfig):
    TESTING = True
    TEST_CONNECTION_STRING = "sqlite:///:memory:"

config = {
    "development": DevelopmentConfig,
    "testing": TestConfig,
    "production": BaseConfig
}

