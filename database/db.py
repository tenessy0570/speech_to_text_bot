from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from config import DB_PATH

engine = create_engine("sqlite:///" + str(DB_PATH), echo=True)
db_session = Session(engine)
