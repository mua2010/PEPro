from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

def index(request):
    template = loader.get_template("index.html")
    return HttpResponse(template.render({}, request))

def welcome_page(request):
    return HttpResponse("This is the PEPro Main page!Actions below:")
def request_review(request):
    return HttpResponse("Request review")

def give_review(request):
    return HttpResponse("Give review to...")