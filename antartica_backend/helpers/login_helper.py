from django.conf import settings

import logging
import jwt
import datetime
import hashlib


from antartica_backend.helpers.query_helper import get_raw_employee
from sqlalchemy import exc

from antartica_backend.common import messages

from rest_framework.response import Response
from rest_framework import status
from rest_framework import exceptions

# create a session for sql alchemy
session = settings.DB_SESSION


# Get an instance of logger
logger = logging.getLogger('employees')

def generate_access_token(user):

    access_token_payload = {
        'user_id': user.id,
        'exp': datetime.datetime.utcnow() + 
                datetime.timedelta(days=0, minutes=15),
        'iat': datetime.datetime.utcnow()
    }
    access_token = jwt.encode(access_token_payload,
                            settings.SECRET_KEY, 
                            algorithm='HS256').decode('utf-8')
    return access_token


def generate_refresh_token(user):
    refresh_token_payload = {
        'user_id': user.id,
        'exp': datetime.datetime.utcnow() + 
                datetime.timedelta(days=0,minutes=30),
        'iat': datetime.datetime.utcnow()
    }
    refresh_token = jwt.encode(
        refresh_token_payload, settings.SECRET_KEY, 
        algorithm='HS256').decode('utf-8')

    return refresh_token

def login_request(self,request):
    try:
        email = request.data.get('email')
        password = request.data.get('password')
        
        if (email is None) or (password is None):
            return Response({"success" : False,
                            "status_code" :status.HTTP_200_OK,
                            "message" : messages.AUTHENTICATION_INVALID,
                            "data" : "None"}, 
                            status=status.HTTP_200_OK)

        user = get_raw_employee(email = email)
        if(user is None):
            return Response({"success" : False,
                            "status_code" :status.HTTP_200_OK,
                            "message" : messages.USER_NOT_FOUND,
                            "data" : None}, 
                            status=status.HTTP_200_OK)

        if user.password != hashlib.md5(str(password).encode()
                            ).hexdigest():
            return Response({"success" : False,
                            "status_code" :status.HTTP_400_BAD_REQUEST,
                            "message" : messages.PASSWORD_INVALID,
                            "data" : None}, 
                            status=status.HTTP_400_BAD_REQUEST)

        access_token = generate_access_token(user)
        refresh_token = generate_refresh_token(user)

        data = {
            'refresh_token' : refresh_token,
            'access_token': access_token,
        }
        return Response({"success" : True,
                        "status_code" :status.HTTP_201_CREATED,
                        "message" : messages.ACCESS_GRANTED,
                        "data": data},status=status.HTTP_201_CREATED)

    except Exception as e:
        logger.error(e)
        session.rollback()
        return Response({"success" : False, 
                "status_code" :status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message" : messages.INTERNAL_SERVER_ERROR,
                "data":None},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)