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
    user = Employee.objects.get(id=13)
    manager = Employee.objects.get(id=user.manager_id)
    underlings = Employee.objects.filter(manager_id=user.id)
    isManager = (len(underlings) != 0)
    context = {
        "manager":manager,
        "user": user,
        "isManager": isManager,
        "manager": manager,
    }
    return render(request, "homepage/homepage.html", context)

def account_info(request):
    user = Employee.objects.get(id=13)
    manager = Employee.objects.get(id = user.manager_id)
    review_count = Review.objects.filter(reviewer=user, status=Review.SENT).count()
    reviewee_count = Review.objects.filter(reviewee=user, status=Review.SENT).count()
    request_count = Request.objects.filter(requestee=user, status=Request.PENDING).count()
    requestee_count = Request.objects.filter(requestor=user).count()
    underlings = list(Employee.objects.filter(manager_id=user.id))
    isManager = (len(underlings) != 0)
    context = {
        "manager":manager,
        "user": user,
        "review_count":review_count,
        "reviewee_count":reviewee_count,
        "request_count":request_count,
        "requestee_count":requestee_count,
        "isManager":isManager,
    }
    return render(request, "homepage/account_info.html", context)



def display_reviews(request):
    user = Employee.objects.get(id=13)
    underlings = Employee.objects.filter(manager_id=user.id)
    isManager = (len(underlings) != 0)
    context = {
        "user": user,
        "reviews": Review.objects.filter(reviewee=user, status=Review.SENT).order_by('-updated_at'),
        "isManager": isManager,

    }
    return render(request, "homepage/display_reviews.html", context)


def display_manager_reviews(request):
    user = Employee.objects.get(id=13)
    underlings = list(Employee.objects.filter(manager_id=13).order_by('last_name'))
    #underlingIds = underlings.values_list('id', flat=True)
    reviews = Review.objects.filter(reviewee__in=underlings, status='S')
    #print (reviews)
    numRevs = ""
    for underl in underlings:
        numRevs+=str(underl.id) + ":" + str(Review.objects.filter(reviewee=underl, status=Review.SENT).count()) + ","
    isManager = (len(underlings) != 0)

    context = {
        "user": user,
        "reviews": reviews,
        "underlings": underlings,
        "numRevs": numRevs,
        "isManager": isManager,
    }
    return render(request, "homepage/display_manager_reviews.html", context)


def view_sent_reviews(request):
    user = Employee.objects.get(id=13)
    reviews = Review.objects.filter(reviewer=user, status='S')
    underlings = list(Employee.objects.filter(manager_id=user.id))
    isManager = (len(underlings) != 0)
    context = {
        "user": user,
        "reviews": reviews,
        "isManager":isManager,
    }
    return render(request, "homepage/view_sent_reviews.html", context)


def display_requests(request):
    user = Employee.objects.get(id=13)
    underlings = list(Employee.objects.filter(manager_id=user.id))
    isManager = (len(underlings) != 0)
    context = {
        "user": user,
        "reviews": Review.objects.filter(reviewee=user, status=Review.SENT).order_by('-updated_at'),
        "drafts": Review.objects.filter(reviewer=user, status=Review.EDITING).order_by('-updated_at'),
        "requests": Request.objects.filter(requestee=user, status=Request.PENDING).order_by('-created_at'),
        "drafts_count": Review.objects.filter(reviewer=user, status=Review.EDITING).count(),
        "requests_count": Request.objects.filter(requestee=user, status=Request.PENDING).count(),
        "isManager": isManager,
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
        
        requestor_id = Employee.objects.get(id=curr_request.requestor_id)
        requestee_id = Employee.objects.get(id=curr_request.requestee_id)

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
    u_id=13
    user = Employee.objects.get(id=u_id)
    '''
    following is a way to only show options with no reveiw requests
    '''
    objects_to_exclude = Request.objects.filter(requestor=user)
    employees_to_exclude = [o.requestee.id for o in objects_to_exclude] 
    employees_to_exclude+=[u_id] # exclude current user as well
    employees = Employee.objects.exclude(id__in=employees_to_exclude).filter(company=user.company).order_by("first_name")

    '''
    show all emps except current user (and give feedback)
    '''
    # employess = Employee.objects.order_by("first_name").exclude(id=100)
    underlings = list(Employee.objects.filter(manager_id=user.id))
    isManager = (len(underlings) != 0)
    context = {
        "user": user,
        "employees": employees,
        "isManager":isManager,
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

# # ===========================================================
# # Not sure if this should be a view but it was how I figured out how to run a script

def insert_employees(request):
    from insert_employees import insert_employees
    insert_employees(json_file_name="employees.json")
    return HttpResponse("Inserted employees")

# def login(request):
    
# 	return render(request, "login.html", {'form':form})

# def insert_employees(request):
#     from insert_employees import insert_employees
#     insert_employees(json_file_name="employees.json")
#     return HttpResponse("Inserted employees")
