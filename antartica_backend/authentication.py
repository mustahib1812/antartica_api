import jwt
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from django.conf import settings

from rest_framework.response import Response
from rest_framework import status
from antartica_backend.common import messages
from antartica_backend.helpers.query_helper import get_raw_employee




class SafeJWTAuthentication(BaseAuthentication):
    """
    Default Authentication Class for REST APIs 


    JWT (Json Web Tokens) Authentication is done by passing the Access
    Token in the 'authentication method'

    methods
    """
    def authenticate(self, request):
        """
        Default method used to authenticate API Tokens sent in Header

        """
        try:
            authorization_header = request.headers.get('Authorization')
            if authorization_header:
                access_token = authorization_header.split(' ')[1]
                payload = jwt.decode(access_token, settings.SECRET_KEY, 
                            algorithms=['HS256'])
                
                
                user_type= payload.get('type')

                user = get_user_object(user_id = payload.get('user_id'),
                user_type=user_type)
                
                if user:
                    return (user, None)
                
                raise exceptions.NotFound({
                    "success" : False,
                    "status_code" :status.HTTP_404_NOT_FOUND,
                    "message" : messages.USER_NOT_FOUND,
                    "data" : None
                })
                

            raise exceptions.AuthenticationFailed({
                "success": False ,
                "status_code":status.HTTP_403_FORBIDDEN,
                "message":messages.AUTHENTICATION_INVALID,
                "data" : None
            })

        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed({"success": False , 
                    "status_code":status.HTTP_403_FORBIDDEN,
                    "message":messages.ACCESS_TOKEN_EXPIRED,
                    "data" : None})
          
        except jwt.InvalidSignatureError:
            raise exceptions.AuthenticationFailed({"success": False , 
                    "status_code":status.HTTP_403_FORBIDDEN,
                    "message":messages.TOKEN_INVALID,
                    "data" : None})

        except jwt.DecodeError:
            raise exceptions.AuthenticationFailed({"success": False , 
                    "status_code":status.HTTP_403_FORBIDDEN,
                    "message":messages.DECODE_ERROR,
                    "data" : None})

        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed({"success": False , 
                    "status_code":status.HTTP_403_FORBIDDEN,
                    "message":messages.TOKEN_INVALID,
                    "data" : None})