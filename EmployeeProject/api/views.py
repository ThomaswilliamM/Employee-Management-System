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

    @action(methods=['GET'], detail=False)
    def getEmployee(self, request):
        try:
            employee = Employee.objects.all()
            empSerializer = EmployeeSerializer(employee, many=True, context = {"request":request})
            return Response(empSerializer.data)
        except:
            return Response({
                        "message": "Something went Wrong"
                    })   
        
    
    @action(methods=['DELETE'], detail=True)
    def deleteWithId(self, request, pk = None):
        try:
            if pk is None:
                return Response({
                            "message": "Give Employee Id"
                        })   
            employee = Employee.objects.filter(employee_id = pk)
            if len(employee) == 0:
                return Response({
                            "message": "No Employee found with given Id"
                        })  
            employee.delete() 
            return Response({
                "message": "Employee deleted succesfully"
            })
        except:
             return Response({
                        "message": "Something went Wrong"
                    })   
    
    @action(methods=['DELETE'], detail=False)
    def deleteWithEmail(self, request):
        try:
            email = request.GET.get('email')
            if email == None:
                return Response({
                        "message": "Please provide an email address."
                    })    
            employee = Employee.objects.filter(email = email)
            if len(employee) == 0:
                return Response({
                        "message": "No employee exist with this emailId"
                    })   
            employee.delete() 
            return Response({
                        "message": "Employee deleted succesfully"
                    })   
        except Exception:
             return Response({
                        "message": "Something went wrong."
                    })   
            
    
    @action(methods=['POST'], detail=False)
    def addEmployee(self, request):
        try:
            data = request.data

            first_name = data.get('first_name')
            last_name = data.get('last_name')
            email = data.get('email')
            contact = data.get('contact')

            employee = Employee(first_name=first_name, last_name=last_name, email=email, contact=contact, employee_id = self.generateEId())
            
            print(employee)
            
            errors = self.validateEmployeeCreation(employee=employee)
            print(errors)
            if not errors:
                employee.save()
                return Response({"message": "Success"})
            else:
                return Response({"errors": errors})    
        except:
            return Response({
                        "error": "Something went Wrong"
                    })   
    
    @action(methods=['put'], detail=True)   
    def editEmployeeWithEmpId(self, request, pk = None):
        try:
            employee = Employee.objects.filter(employee_id = pk)
            if (len(employee)==0):
                
                return Response({
                            "error": "Employee id not found."
                        })

            content = request.data
            employee = employee[0]

            employee.email = content.get("email", employee.email)
            employee.first_name = content.get("first_name", employee.first_name)
            employee.last_name = content.get("last_name", employee.last_name)
            employee.contact = content.get("contact", employee.contact)

            errors = self.validateEmployeeEdit(employee=employee)
            if not errors:
                employee.save()
                return Response({"message": "Success"})
            else:
                return Response({"errors": errors})
        except:
            return Response({
                        "error": "Something went Wrong"
                    })
    
    @action(methods=['PUT'], detail=False)
    def editEmployeeWithEmail(self, request):
        try:
            email = request.GET.get('email')
            employee = Employee.objects.filter(email = email)[0]
            content = request.data
            if employee == None:
            
                return Response({
                            "error": "No employee found with given email. "
                        })

            employee.first_name = content.get("first_name", employee.first_name)
            employee.last_name = content.get("last_name", employee.last_name)
            employee.contact = content.get("contact", employee.contact)


            errors = self.validateEmployeeEdit(employee=employee)
            if not errors:
                employee.save()
                return Response({"message": "Success"})
            else:
                return Response({"errors": errors})
        except:
            return Response({
                        "error": "Something went Wrong"
                    })


    def generateEId(self):
        employees = Employee.objects.all()
        s = set()
        for i in employees:
            s.add(i.employee_id)
        while True:
            x = random.randint(1,100)
            if "e"+str(x) not in s:
                break
        return "e"+str(x)
    
    def validateEmployeeCreation(self, employee):
        errors = {}
        employees = Employee.objects.all()
        resultSet = {"email":set(), "contact":set()}
        for i in employees:
            resultSet["email"].add(i.email)
            resultSet["contact"].add(i.contact)

        if(not re.match("^[A-Za-z.]+$" , employee.first_name)):
            if "first_name" not in errors:
                errors["first_name"] = set()
            errors["first_name"].add("first name can only contain alphabets or .. ")
        if(not re.match("^[A-Za-z.]+$" , employee.last_name)):
            if "last_name" not in errors:
                errors["last_name"] = set()
            errors["last_name"].add("last name can only contain alphabets or .. ")
        if(not re.match(".*@.*\.com$" , employee.email)):
            if "email" not in errors:
                errors["email"] = set()
            errors["email"].add("email should contain @ and end with .com. ")
        if (employee.email in resultSet["email"]):
            if "email" not in errors:
                errors["email"] = set()
            errors["email"].add("EmailId already exists. ")
        if(not employee.contact.isnumeric() or len(employee.contact)!=10):
            if "contact" not in errors:
                errors["contact"] = set()
            errors["contact"].add("Contact number should be a 10 digit number. ")
        if (employee.contact in resultSet["contact"]):
            if "contact" not in errors:
                errors["contact"] = set()
            errors["contact"].add("contact number already exists. ")
        return errors
    
    def validateEmployeeEdit(self, employee):
        errors = {}
        
        resultSet = {"email":set(), "contact":set()}
        

        if(not re.match("^[A-Za-z.]+$" , employee.first_name)):
            if "first_name" not in errors:
                errors["first_name"] = set()
            errors["first_name"].add("first name can only contain alphabets or .. ")
        if(not re.match("^[A-Za-z.]+$" , employee.last_name)):
            if "last_name" not in errors:
                errors["last_name"] = set()
            errors["last_name"].add("last name can only contain alphabets or .. ")
        if(not re.match(".*@.*\.com$" , employee.email)):
            if "email" not in errors:
                errors["email"] = set()
            errors["email"].add("email should contain @ and end with .com. ")
        
        if(not employee.contact.isnumeric() or len(employee.contact)!=10):
            if "contact" not in errors:
                errors["contact"] = set()
            errors["contact"].add("Contact number should be a 10 digit number. ")
        
        return errors




           

