from django.conf import settings
from django.http import HttpResponse

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from rest_framework.renderers import TemplateHTMLRenderer

from django.template import loader
from antartica_backend.helpers.add_details import post_details


class Register(APIView):
    """
    This class adds the details into table

    Methods
    -------
    POST:
    Parameter : first_name, last_name, email_id, 
    password, organization_name

    """
    permission_classes = (AllowAny,)
    authentication_classes = ()

    def post(self, request):
        """
        Method : POST
        Create new object in the employee table.
        -------

        Parameters:
        Mandatory fields in json format.

        Returns:
        json: success message.

        """
        response = post_details(self,request)
        return response 
