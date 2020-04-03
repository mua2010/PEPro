from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.core.exceptions import ObjectDoesNotExist

from .forms import RequestReviewForm
from .models import Review, Request, Employee

def index(request):
    context = {}
    curr_user = Employee.objects.get(id=1)
    context = {'curr_user': curr_user}
    return render(request, 'index.html', context)
    # template = loader.get_template("index.html")
    # return HttpResponse(template.render({}, request))

def request_review(request):
    if request.method == "POST":
        form = RequestReviewForm(request.POST)
        if form.is_valid():
            form.insert()
            form = RequestReviewForm()
    else:
        form = RequestReviewForm()
    return render(request, "request_review.html", {"form": form})

def view_requests(request, email):
    try:
        reviewer = Employee.objects.get(email=email)
    except ObjectDoesNotExist:
        return HttpResponse("Unknown email in url")
    
    requests = Request.objects.filter(request_reviewer=reviewer)
    context = {
        "empty": len(requests) == 0,
        "requests": requests
    }
    return render(request, "view_requests.html", context)

def give_review(request):
    return HttpResponse("Give review to...")


def display_requests(request):
    context = {}
    requests = Request.objects.order_by('id')
    context = {'requests': requests}
    return render(request, 'display_requests.html', context)

# ===========================================================
# Not sure if this should be a view but it was how I figured out how to run a script
def insert_employees(request):
    from insert_employees import insert_employees
    insert_employees(json_file_name="employees.json")
    return HttpResponse("Inserted employees")
