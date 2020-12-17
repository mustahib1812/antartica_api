from antartica_backend.models import Employees
from antartica_backend.common import messages
import logging
from django.conf import settings
import jwt
from rest_framework.response import Response
from django.core.exceptions import PermissionDenied
from rest_framework import exceptions

from antartica_backend.helpers.query_helper import get_raw_employee, get_employee_id
# Get an instance of logger
logger = logging.getLogger('rolespermissions')

# create a session for sql alchemy
session = settings.DB_SESSION

from rest_framework import permissions

class RolePermissionCheck(permissions.BasePermission):
    """
    Check whether user has permissions.
    =====

    Parameter:
    function_slug (string): function_slug as defined in 
    controller_function table

    Returns:
    Boolean : True/False

    """

    def has_permission(self, request, view):

        try: 
            user_id = get_employee_id(request)

            return True
        except Exception as e:
            return False