import contextlib
import logging

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

LOG = logging.getLogger(__name__)

Base = declarative_base()
Session = sessionmaker(expire_on_commit=False)


def configure(engine=None):
    """
    Configure the session-maker with a DB engine.

    Parameters
    ----------
    engine: `SqlAlchemy.Engine`
        Defaults to using a new in memory sqlite DB engine when None.
    """
    if engine is None:
        engine = get_engine()
    create_schema(engine)
    Session.configure(bind=engine)


def get_engine(url='sqlite:///:memory:'):
    """
    Create an Engine.

    Parameters
    ----------
    url: `str`
        Database connection string.

    Returns
    -------
    sqlalchemy.Engine
    """
    return create_engine(url, echo=True)


def create_schema(engine):
    """
    Runs DDL for schema.

    Parameters
    ----------
    engine: `sqlalchemy.Engine`
    """
    from is_ad.model.model import Model
    from is_ad.model.document import Document
    from is_ad.model.view import View


    Base.metadata.create_all(engine)


@contextlib.contextmanager
def session_scope(with_session=None):
    """
    Session scope for transactions.

    Parameters
    ----------
    with_session: `SqlAlchemy.Session`
        Defaults to  new session when None.

    Yields
    ------
    session
    """
    if with_session is not None:
        yield with_session
        return

    with_session = Session()

    try:
        yield with_session
        with_session.commit()
    except Exception:
        with_session.rollback()
        LOG.warning('Encountered problem during session transaction.',
                    exc_info=True)
        raise
    finally:
        with_session.expunge_all()
