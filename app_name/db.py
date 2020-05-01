from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

# because cascade deletes when using mysql need InnoDB engine in order to 
# work correctly, create base abstract class with InnoDB engine
class ModelBase(db.Model):
    __abstract__ = True
    __table_args__ = {
        "mysql_engine": "InnoDB"
    }
