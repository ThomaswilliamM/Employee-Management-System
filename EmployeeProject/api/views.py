import json
import random
import re
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import viewsets

from api.models import Employee
from api.serializers import EmployeeSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import status





class EmployeeView(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

   