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
from antartica_backend.helpers.login_helper import (
    login_request,generate_access_token,generate_refresh_token)


class Login(APIView):
    """
    This class authenticates existing employees and grants an
    access token to fetch list API

    Methods
    -------
    POST:
    Parameter : 
    email_id, password

    """
    permission_classes = (AllowAny,)
    authentication_classes = ()

    def post(self, request):
        """
        Method : POST
        Authenticates employee with credentials
        -------

        Parameters:
        Mandatory fields in json format.

        Returns:
        json: success message.

        """
        response = login_request(self,request)
        return response 

class RefreshToken(APIView):
    """
        This class used to generate a new access token from 
        refresh token when it is expired.

        METHODS
        -------
        POST:
        to give refreshtoken.
    """
    permission_classes = (AllowAny,)
    authentication_classes = ()

    def post(self,request,format=None):
        """
        METHOD: POST

        returns a refresh token
        """
        response = refresh_token(request)
        return response     

class AccessToken(APIView):
    """
        This class used to generate a new access token from 
        refresh token when it is expired.

        METHODS
        -------
        GET:
        to give refreshtoken.
    """

    def get(self,request,format=None):
        """
        METHOD: GET

        returns a refresh token
        """
        response = generate_access_token(request)
        return response     