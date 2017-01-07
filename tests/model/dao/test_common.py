from is_ad.model.dao.common import (
    create_schema,
    get_engine
)


def test_create_schema():
    engine = get_engine('sqlite:///test_schema.db')
    create_schema(engine)
