from sqlalchemy import Sequence, Column, Integer, String, ForeignKey, UniqueConstraint, Index

from is_ad.model.dao.common import Base


class Document(Base):
    __tablename__ = 'document'

    id = Column(Integer, Sequence('document_id_seq'), primary_key=True)
    text = Column(String, nullable=False)
    category = Column(Integer, nullable=False, index=True)
    url = Column(String, nullable=True, index=True)
    model_id = Column(Integer, ForeignKey('model.id'), nullable=False)
    UniqueConstraint('document_url', 'model_id', name='uix_1')

    def __repr__(self):
        return str(self.__dict__)
