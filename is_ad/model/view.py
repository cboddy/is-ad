from sqlalchemy import Sequence, Column, Integer, TIMESTAMP, ForeignKey, Boolean

from is_ad.model.dao.common import Base


class View(Base):
    __tablename__ = 'view'

    id = Column(Integer, Sequence('view_id_seq'), primary_key=True)
    document_id = Column(Integer, ForeignKey('document.id'))
    timestamp = Column(TIMESTAMP, nullable=False)
    user_feedback = Column(Boolean, nullable=True)
