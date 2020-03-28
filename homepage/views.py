from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

def index(request):
    template = loader.get_template("index.html")
    return HttpResponse(template.render({}, request))

def request_review(request):
    return HttpResponse("Request review")

def give_review(request):
    return HttpResponse("Give review to...")