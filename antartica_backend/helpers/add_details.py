from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.conf import settings
from django.http import HttpResponse
from django.db import IntegrityError
import hashlib 

from antartica_backend.models import Employees

from antartica_backend.helpers.query_helper import get_raw_employee
from antartica_backend.common import messages

# create a session for sql alchemy
session = settings.DB_SESSION

def post_details(self, request):

    try:
        first_name = request.data["first_name"]
        last_name = request.data["last_name"]
        organization_name = request.data["organization_name"]
        email = request.data["email"]

        password_hash = hashlib.md5(
            request.data["password"].encode()).hexdigest()

            
        request.data['password'] = password_hash
        
        ex_details = get_raw_employee(email=email)

        if ex_details:
            return Response({
                            "success" : False,
                            "status_code" :status.HTTP_400_BAD_REQUEST,
                            "message" : messages.DUPLICATE_KEY,
                            "data" : None},
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            if request.data and ex_details is None:
                add_details = Employees(**request.data)
                session.add(add_details)
                session.commit()
                

                return Response({
                                "success" : True,
                                "status_code" :status.HTTP_201_CREATED,
                                "message" : messages.EMPLOYEE_ADDED,
                                "data" : None},
                                status=status.HTTP_201_CREATED)
            else:
                session.rollback()
                return Response({
                                "success" : False,
                                "status_code" :status.HTTP_400_BAD_REQUEST,
                                "message" : messages.DETAILS_NEEDED,
                                "data" : None},
                                status=status.HTTP_400_BAD_REQUEST)
    except IntegrityError as e:
        return Response({
                        "success" : False,
                        "status_code" :status.HTTP_400_BAD_REQUEST,
                        "message" : e,
                        "data" : None},
                        status=status.HTTP_400_BAD_REQUEST)