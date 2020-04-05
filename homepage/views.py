from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404

from .forms import RequestReviewForm
from .models import Review, Request, Employee
from django.views.decorators.csrf import csrf_exempt
import json



def index(request):
    context = {}
    curr_user = Employee.objects.get(id=6)
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
    # get_object_or_404
    requests = Request.objects.filter(requestee_id=reviewer)
    context = {
        "empty": len(requests) == 0,
        "requests": requests
    }
    return render(request, "view_requests.html", context)

def give_review(request):
    return HttpResponse("Give review to...")


def display_requests(request):
    context = {}
    # requests = Request.objects.order_by('id')
    # context = {'requests': requests}
    # return render(request, 'display_requests.html', context)
    requests = Request.objects.filter(requestee_id=6)
    # get_object_or_404(queryset, pk=1)

    context = {
        "empty": len(requests) == 0,
        "requests": requests
    }
    return render(request, "display_requests.html", context)

@csrf_exempt
def display_requests_post(request):
    # context = {
    #     "status": "DONE"
    # }
    # if request.method == 'POST':
    #     print("SUCESS FROM VIEWS.py")
    #     # breakpoint()
    #     temp = request.body
    #     print(temp)
    #     pythonObj = json.loads(temp)
    #     print(pythonObj)
        
    
    temp = request.body
    pythonObj = json.loads(temp)
    # breakpoint()
    if request.method == 'POST':
        status = pythonObj.get('status')
        curr_id = int(pythonObj.get('request_id'))
        curr_request = Request.objects.get(id=curr_id)
        # curr_request = Request.objects.get(id=request.POST('id'))
        requestor_id = curr_request.requestor_id
        requestor_id = get_object_or_404(Employee,id=requestor_id)
        requestee_id = curr_request.requestee_id
        requestee_id = get_object_or_404(Employee,id=requestee_id)
        
        # if accepted
        # create a review obj
        if status == True:
            curr_request.status = "accepted"
            curr_request.save()
            Review.objects.create(reviewer=requestee_id, reviewee=requestor_id)

        # if rejected
        # set status of request obj to rejected
        if status == False:
            # curr_request.status = request.POST.get('status')
            curr_request.status = "rejected"
            curr_request.save()

    return HttpResponse(json.dumps({
        "formdata": "FORM_DATA"}),
    content_type="application/json")
    # context = {
        
    # }
    # return context

def accept_decline_review_requests(request):
    # breakpoint()
    if request.method == 'POST':
        curr_request = Request.objects.get(id=request.POST('id'))
        requestor_id = request.POST('requestor_id')
        requestee_id = request.POST('requestee_id')

        # if accepted
        # create a review obj
        if request.POST.get('status') == "Accept":
            curr_request.status = "accepted"
            curr_request.save()
            Review.objects.create(reviewer=requestee_id, reviewee=requestor_id)

        # if rejected
        # set status of request obj to rejected
        if request.POST.get('status') == "Reject":
            # curr_request.status = request.POST.get('status')
            curr_request.status = "rejected"
            curr_request.save()
    # return render(request, "display_requests.html", {})

# ===========================================================
# Not sure if this should be a view but it was how I figured out how to run a script
def insert_employees(request):
    from insert_employees import insert_employees
    insert_employees(json_file_name="employees.json")
    return HttpResponse("Inserted employees")
