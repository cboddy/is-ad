from sqlalchemy import Sequence, Column, Integer, String

from is_ad.model.dao.common import Base


class Model(Base):
    __tablename__ = 'model'

    id = Column(Integer, Sequence('model_id_seq'), primary_key=True)
    name = Column(String, nullable=False, unique=True)

    def __repr__(self):
        return str(self.__dict__)

