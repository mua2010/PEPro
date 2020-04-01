from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from .forms import RequestReviewForm
from .models import Review

def index(request):
    template = loader.get_template("index.html")
    return HttpResponse(template.render({}, request))

def request_review(request):
    if request.method == "POST":
        form = RequestReviewForm(request.POST)

        if form.is_valid():
            form.insert()
            form = RequestReviewForm()
            render(request, "request_review.html", {"form": form, "confirmation":True})
    else:
        form = RequestReviewForm()
    
    return render(request, "request_review.html", {"form": form})

def give_review(request):
    return HttpResponse("Give review to...")

# Not sure if this should be a view but it was how I figured out how to run a script
def insert_employees(request):
    from insert_employees import insert_employees
    insert_employees(json_file_name="employees.json")
    return HttpResponse("Inserted employees")
