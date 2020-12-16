def serialize_sqlalchemy(object):
    return [ row._asdict() for row in object ]
