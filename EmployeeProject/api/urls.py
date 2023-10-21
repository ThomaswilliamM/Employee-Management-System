from django.contrib import admin
from django.urls import include, path
from EmployeeProject.views import home_page
from api.views import EmployeeView
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'employees',EmployeeView)

urlpatterns = [

    path("", include(router.urls)),

    
]