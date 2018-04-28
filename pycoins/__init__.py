from pycoins import utils
from pycoins import models
from sqlalchemy.orm import sessionmaker


CONFIG = utils.load_config()
ENGINE = utils.init_db_engine(CONFIG)
models.BaseModel.metadata.create_all(ENGINE)
Session = sessionmaker()
Session.configure(bind=ENGINE)
