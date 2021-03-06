"""record_keeper URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework_swagger.views import get_swagger_view

from call_records.api.viewsets import CallRecordViewSet
from telephone_bill.api.viewsets import TelephoneBillViewSet

router = routers.DefaultRouter()
router.register(r'CallRecords', CallRecordViewSet, base_name='CallRecord')
router.register(r'TelephoneBill', TelephoneBillViewSet, base_name='TelephoneBill')
schema_view = get_swagger_view(title='Record Keeper')


urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('docs/', schema_view)
]
