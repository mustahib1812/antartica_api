from django.conf import settings
from django.http import HttpResponse

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView


from rest_framework.renderers import TemplateHTMLRenderer

from django.template import loader
from antartica_backend.helpers.add_details import post_details


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

    authentication_classes = (SafeJWTAuthentication,)

    def get(self, request):
        """
        Method : GET
        Fetches an employee object
        -------

        Parameters:
        Mandatory fields in json format.

        Returns:
        json: success message.

        """
        # response = post_details(self,request)
        return HttpResponse("Get Employee") 
