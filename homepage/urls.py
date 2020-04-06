"""pepro URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name="homepage"),
    path('request_review', views.request_review, name="request_review"),
    path('view_requests/<str:email>', views.view_requests, name="view_request"),
    path('give_review/<int:review_id>', views.give_review, name="give_review"),
    path('insert_employees', views.insert_employees, name="insert_employees"),
    path('display_requests', views.display_requests, name="display_requests"),
]
