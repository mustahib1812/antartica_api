from antartica_backend.models import Employees
from antartica_backend.helpers.serializer_helper import serialize_sqlalchemy

from sqlalchemy import exc, or_ , case, func
from sqlalchemy.orm import aliased
import logging
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from rest_framework.response import Response
from rest_framework import status


# create a session for sql alchemy
session = settings.DB_SESSION

# Instance of logger for Class Partners
logger = logging.getLogger('employees')

def get_raw_employee(email=None, id=None):
    """
    Returns a raw employee object.

    Parameter:
    details: 

    Response:
    sqlalchemy object

    """
    try:
        if email:
            raw_employee = session.query(Employees).filter(Employees.email==email).one_or_none()
            session.commit()
        
        if id:
            raw_employee = session.query(Employees).filter(Employees.id==id).one_or_none()
            session.commit()
        
    except Exception as e:
        session.rollback()
        raw_employee = None

    return raw_employee

def get_employee_id(request):
    try:
        authorization_header = request.headers.get('Authorization')
        if authorization_header:
            access_token = authorization_header.split(' ')[1]
            payload = jwt.decode(access_token, 
            settings.SECRET_KEY, algorithms=['HS256'])
            user_id = payload.get('user_id')
            return user_id
        return None

    except Exception as e :
        logger.error(e)
        return None

def get_employees(self, request, employee_id=None):
    """
    Returns an emoloyee object or a list.

    Parameter:
    details: 

    Response:
    sqlalchemy object

    """
    try:

        page_num = request.query_params.get('page', 1)
        first_name = request.query_params.get('first_name')
        last_name = request.query_params.get('last_name')


        if employee_id:
            employees = fetch_employees(employee_id)
        else:
            employees = fetch_employees(first_name=first_name, last_name=last_name)

        if employees:
             # pagination
            paginator = Paginator(employees, 10)
            try:
                employees = paginator.page(page_num)
            except PageNotAnInteger:
                employees = paginator.page(1)
            except EmptyPage:
                return Response({"success" : False, 
                        "status_code" :status.HTTP_200_OK,
                        "message" : "Employees List Exhausted- No data on this page",
                        "data":None},
                        status=status.HTTP_200_OK)

            serializer = serialize_sqlalchemy(employees)

            return Response({"success" : True,
                    "status_code" :status.HTTP_200_OK,
                    "message" : "DATA FOUND",
                    "data" :serializer},
                    status=status.HTTP_200_OK)

            
        else:
            return Response({"success" : False, 
                        "status_code" :status.HTTP_200_OK,
                        "message" : "No Data Found",
                        "data":None},
                        status=status.HTTP_200_OK)

        
   
    except Exception as e:
        session.rollback()
        employees = None


    return employees



def fetch_employees(employee_id=None, first_name=None, last_name=None):

    try:
        employees = session.query(
            Employees.first_name.label("First Name"),
            Employees.last_name.label("Last Name"),
            Employees.email.label("Email ID"),
            Employees.organization_name.label("Organization Name"),
        )

        if employee_id:
            employees = employees.filter(Employees.id==employee_id)
        
        else:
            if first_name:
                employees = employees.filter(
                    Employees.first_name.contains(first_name)
                    )
            if last_name:
                employees = employees.filter(
                    Employees.last_name.contains(last_name)
                    )
        employees = employees.all()     
        session.commit()

    except Exception as e:
        logger.error(e)
        session.rollback()
        employees = None

    return employees