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

app_name = 'homepage'

urlpatterns = [
    path('', views.homepage, name="homepage"),
    path('display_requests', views.display_requests, name="display_requests"),
    path('display_reviews', views.display_reviews, name="display_reviews"),
    path('request_review', views.request_review, name="request_review"),
    path('account_info', views.account_info, name="account_info"),
    path('display_manager_reviews', views.display_manager_reviews, name="display_manager_reviews"),
    path('view_sent_reviews', views.view_sent_reviews, name="view_sent_reviews"),
    
    path('accept_deny_request', views.accept_deny_request, name="accept_deny_request"),
    path('submit_requests', views.submit_requests, name="submit_requests"),
    path('submit_draft_post', views.submit_draft_post, name="submit_draft_post"),
]
