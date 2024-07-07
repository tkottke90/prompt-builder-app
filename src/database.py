from typing import Any, Callable
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import Session, scoped_session, sessionmaker
from src.models.base_model import Base
import src.models

QueryFn = Callable[[Session], Any]

engine = create_engine("sqlite:///var/ai-api", echo=True, logging_name="database")

def initialize():
  Base.metadata.create_all(bind=engine)

def query(fn: QueryFn):
  session = Session(engine)
  try:
    fn(session)
  finally:
    session.commit()
    session.close()

def transaction():
  def functionCollector(fn):
    def functionWrapper(*args, **kwargs):
      with Session(engine, expire_on_commit=False) as session:
        try:
          results = fn(*args, session=session, **kwargs)
          session.commit()

          return results
        except Exception as e:
          session.rollback()
          raise e
        finally:
          session.close()


    return functionWrapper
  return functionCollector