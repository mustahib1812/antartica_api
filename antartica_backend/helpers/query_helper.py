from antartica_backend.models import Employees
from antartica_backend.helpers.serializer_helper import serialize_sqlalchemy

from sqlalchemy import exc, or_ , case, func
from sqlalchemy.orm import aliased
import logging
from django.conf import settings


# create a session for sql alchemy
session = settings.DB_SESSION

def get_raw_employee(email):
    """
    Returns a raw employee object.

    Parameter:
    details: 

    Response:
    sqlalchemy object

    """
    try:
        raw_employee = session.query(Employees).filter(Employees.email==email).one_or_none()
        session.commit()
        
    except Exception as e:
        session.rollback()
        raw_employee = None

    return raw_employee