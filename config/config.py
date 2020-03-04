# env based config overrides
import os
from flask_dotenv import DotEnv

class BaseConfig(object):
    ENV = "development"
    MY_VARIABLE = "Petrica"
    DEBUG = True

    @classmethod
    def init_app(self, app):
        env = DotEnv()
        path = os.getcwd().replace("config", "")
        env.init_app(app, env_file=os.path.join(path, ".env"), verbose_mode=True)

class DevelopmentConfig(BaseConfig):
    MY_DEV_VARIABLE = "Cojones!"

class TestConfig(BaseConfig):
    TESTING = True

config = {
    "development": DevelopmentConfig,
    "testing": TestConfig,
    "production": BaseConfig
}