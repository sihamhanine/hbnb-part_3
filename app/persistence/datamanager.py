from config import Config, db
from sqlalchemy.orm import sessionmaker
import datetime

Session = sessionmaker(bind=Config.engine)
session = Session()

class DataManager:
    def save(entity, session):
        try:
            session.add(entity)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e

    def read(entity):
        result = {}
        for key, value in entity.__dict__.items():
            if key != '_sa_instance_state':
                if isinstance(value, datetime.datetime):
                    result[key] = value.isoformat()
                else:
                    result[key] = value
        return result

    def update(entity, updates, session):
        try:
            entity = session.merge(entity)
            for key, value in updates.items():
                if hasattr(entity, key):
                    setattr(entity, key, value)

            session.commit()
        except Exception as e:
            session.rollback()
            raise e

    def delete(entity, session):
        try:
            session.delete(entity)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
