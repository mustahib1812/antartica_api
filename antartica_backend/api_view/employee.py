from django.conf import settings
from django.http import HttpResponse

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

import logging

from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.permissions import IsAuthenticated,AllowAny


from antartica_backend.permissions import RolePermissionCheck

from django.template import loader
from antartica_backend.helpers.add_details import post_details
from antartica_backend.helpers.query_helper import get_employees


# Getting instance of logger for class Partners
logger = logging.getLogger("employees")

class Employee(APIView):
    """
    This class fetches the list of employees 
    and works with filters and pagination

    Methods
    -------
    POST:
    Parameter for search filter: 
    first_name, last_name, email_id, organization_name

    """

    permission_classes = (AllowAny,)
    authentication_classes = ()

    def get(self, request, employee_id=None):
        """
        Method : GET
        Return a list of all the employees in system or
        a specific employee if the unique id for that emoloyee is 
        provided.

        Can handle additional filters (search) parameters
        viz - first_name, last_name, email_id, organization_name

        -------

        Parameters:
        employee_id :  unique id of employee

        Returns:
        json: list of employees or a single employee.
        """

        try:

            result = get_employees(self,request, employee_id)
            return result 
        
        except Exception as e:
            logger.error('EMPLOYEE API VIEW : {}'.format( e))
                
