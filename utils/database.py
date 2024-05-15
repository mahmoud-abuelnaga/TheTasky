# external modules
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import event

# constants
DATABASE_IP = "localhost"
DATABASE_NAME = "task_management"
## postgress connect
# SQLALCHEMY_DATABASE_URL = f"postgresql://{os.getenv("user_name")}:{os.getenv("password")}@{DATABASE_IP}/{DATABASE_NAME}"
## sqlite connect
SQLALCHEMY_DATABASE_URL = "sqlite:///./task_management.db"


def _fk_pragma_on_connect(dbapi_con, con_record):
    dbapi_con.execute("pragma foreign_keys=ON")


# setup database
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

## sqlite enforce foreign keys
event.listen(engine, "connect", _fk_pragma_on_connect)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def getSession():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def getBase():
    return Base


def getEngine():
    return engine
