import json

from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt, csrf_protect

from .forms import RequestReviewForm, GiveReviewForm, NameBox
from .models import Review, Request, Employee


def homepage(request):
    user = Employee.objects.get(id=100)
    context = {
        "user": user,
    }
    return render(request, "homepage/homepage.html", context)



def display_reviews(request):
    user = Employee.objects.get(id=100)
    context = {
        "user": user,
        "reviews": Review.objects.filter(reviewee=user, status=Review.SENT).order_by('-updated_at'),
    }
    return render(request, "homepage/display_reviews.html", context)



def display_requests(request):
    user = Employee.objects.get(id=100)
    context = {
        "user": user,
        "reviews": Review.objects.filter(reviewee=user, status=Review.SENT).order_by('-updated_at'),
        "drafts": Review.objects.filter(reviewer=user, status=Review.EDITING).order_by('-updated_at'),
        "requests": Request.objects.filter(requestee=user, status=Request.PENDING).order_by('-created_at')
    }
    return render(request, "homepage/display_requests.html", context)

@csrf_exempt
def accept_deny_request(request):
    data = request.POST
    
    if Request.objects.filter(id=data["request_id"], status=Request.PENDING).exists():
        curr_request = Request.objects.get(id=data["request_id"], status=Request.PENDING)
        status = data["status"]
        curr_request.status = status
        curr_request.save()
        
        requestor_id = get_object_or_404(
            Employee, id=curr_request.requestor_id)
        requestee_id = get_object_or_404(
            Employee, id=curr_request.requestee_id)

    response_data = {
        "feedback": None,
        "id": None
    }
    if status == "A":
        review = Review.objects.create(reviewer=requestee_id, reviewee=requestor_id)
        response_data["feedback"] = "Request Accepted"
        response_data["id"] = review.id
        response_data["reviewee"] = str(review.reviewee)
        return HttpResponse(json.dumps(response_data))
    elif status == "D":
        response_data["feedback"] = "Request Rejected"
        return HttpResponse(json.dumps(response_data))

@csrf_exempt
def submit_draft_post(request):
    data = request.POST
    review = Review.objects.get(id=data["review_id"])
    status = data["status"]
    review.status = status
    review.text = data["draft_text"]
    review.save()

    if status == "S":
        return HttpResponse("Review sent")
    elif status == "E":
        return HttpResponse("Draft Saved")


@csrf_exempt
def request_review(request):
    user = Employee.objects.get(id=100)
    '''
    following is a way to only show options with no reveiw requests
    '''
    objects_to_exclude = Request.objects.filter(requestor=user)
    employees_to_exclude = [o.requestee.id for o in objects_to_exclude] 
    employees_to_exclude+=[100] # exclude current user as well
    employees = Employee.objects.exclude(id__in=employees_to_exclude).order_by("first_name")

    '''
    show all emps except current user (and give feedback)
    '''
    # employess = Employee.objects.order_by("first_name").exclude(id=100)
    # breakpoint()
    context = {
        "user": user,
        "employees": employees
    }
    return render(request, "homepage/request_review.html", context)

@csrf_exempt
def submit_requests(request):
    # breakpoint()
    response_data = {
        "feedback": None,
        "private_status": None
    }
    
    employees = request.POST.getlist("employees[]")
    if not employees:
        response_data["feedback"] = "Please select atleast one empolyee!"
        response_data["private_status"] = 204
        return HttpResponse(json.dumps(response_data))

    reviewee_id = request.POST["reviewee_id"]

    reviewee = Employee.objects.get(id=reviewee_id)
    for e_id in employees:
        if not Employee.objects.filter(id=e_id).exists():
            response_data["feedback"] = "Employee does not exist!"
            response_data["private_status"] = 401
            return HttpResponse(json.dumps(response_data))

        reviewer = Employee.objects.get(id=e_id)
        if Request.objects.filter(requestor=reviewee, requestee=reviewer).exists():
            status_text = "There is already a pending review request to " +  reviewer.first_name + " " + reviewer.last_name + "!"
            response_data["feedback"] = status_text
            response_data["private_status"] = 401
            return HttpResponse(json.dumps(response_data))

        if reviewee_id == reviewer.id:
            response_data["feedback"] = "You cannot review yourself!"
            response_data["private_status"] = 401
            return HttpResponse(json.dumps(response_data))

        reviewer = Employee.objects.get(id=e_id)
        Request.objects.create(requestee=reviewer, requestor=reviewee)

    response_data["feedback"] = "Request sent!"
    response_data["private_status"] = 200
    return HttpResponse(json.dumps(response_data))

@csrf_exempt
def request_review_post(request):
    reviewee_email = request.POST["reviewee_email"]
    reviewer_email = request.POST["reviewer_email"]

    if not Employee.objects.filter(email=reviewer_email).exists():
        return HttpResponse("Co-worker's email does not match any emails on record!")

    reviewee = Employee.objects.get(email=reviewee_email)
    reviewer = Employee.objects.get(email=reviewer_email)
    if Request.objects.filter(requestor=reviewee, requestee=reviewer).exists():
        return HttpResponse("There is already a pending review request to this person!")

    if reviewee_email == reviewer_email:
        return HttpResponse("You cannot review yourself!")

    reviewee = Employee.objects.get(email=reviewee_email)
    reviewer = Employee.objects.get(email=reviewer_email)

    Request.objects.create(requestee=reviewer, requestor=reviewee)

    return HttpResponse("Request sent.", status=200)


# # ===========================================================
# # Not sure if this should be a view but it was how I figured out how to run a script

# def insert_employees(request):
#     from insert_employees import insert_employees
#     insert_employees(json_file_name="employees.json")
#     return HttpResponse("Inserted employees")
