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
        "reviews": Review.objects.filter(reviewee=user, status=Review.SENT),
        "drafts": Review.objects.filter(reviewer=user, status=Review.EDITING),
        "requests": Request.objects.filter(requestee=user, status=Request.PENDING)
    }
    return render(request, "homepage.html", context)


def request_review_post(request):
    reviewee_email = request.POST["reviewee_email"]
    reviewer_email = request.POST["reviewer_email"]

    if not Employee.objects.filter(email=reviewer_email).exists():
        return HttpResponse("Co-Worker's email does match any emails on record")

    reviewee = Employee.objects.get(email=reviewee_email)
    reviewer = Employee.objects.get(email=reviewer_email)
    if Request.objects.filter(requestor=reviewee, requestee=reviewer).exists():
        return HttpResponse("There is already a pending review request to this person")

    if reviewee_email == reviewer_email:
        return HttpResponse("You cannot review yourself")

    reviewee = Employee.objects.get(email=reviewee_email)
    reviewer = Employee.objects.get(email=reviewer_email)

    Request.objects.create(requestee=reviewer, requestor=reviewee)

    return HttpResponse("Request sent.", status="test")


'''
{
    csrfmiddlewaretoken: "{{ csrf_token }}",
    request_id: request_id,
    status: status,
}
'''
def accept_deny_request(request):
    data = request.POST
    curr_request = Request.objects.get(id=data["request_id"])
    status = data["status"]
    curr_request.status = status
    curr_request.save()
    
    requestor_id = get_object_or_404(
        Employee, id=curr_request.requestor_id)
    requestee_id = get_object_or_404(
        Employee, id=curr_request.requestee_id)

    if status == "A":
        Review.objects.create(reviewer=requestee_id, reviewee=requestor_id)
        return HttpResponse("Request Accepted")
    elif status == "D":
        return HttpResponse("Request Rejected")


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

# =========================================
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
    if request.method == "POST":
        request_id = int(request.POST["request_id"])
        accepted = bool(request.POST["accepted"])
        review_request = Request.objects.get(id=request_id)
        review_id_str = ""
        if accepted:
            review = Review.objects.create(
                reviewer=review_request.request_reviewer,
                reviewee=review_request.request_reviewee,
            )
            review_id_str = str(review.id)
        review_request.delete()
        # TODO if accepted is false send a message to the requestor saying their request was denied
        return HttpResponse("{\"review_id\": " + review_id_str + "}")

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


def give_review(request, review_id):
    review = Review.objects.get(id=review_id)
    form = GiveReviewForm(initial={"review_text": review.review_text})
    context = {
        "reviewee_name": str(review.reviewee),
    }
    return render(request, "give_review.html", context)


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


def display_requests_helper(id):
    reviewer = get_object_or_404(Employee, id=id)

    requests = Request.objects.filter(requestee_id=reviewer)
    context = {
        "empty": len(requests) == 0,
        "requests": requests
    }
    # return render(request, "view_requests.html", context)
    return context
# ===========================================================
# Not sure if this should be a view but it was how I figured out how to run a script


def insert_employees(request):
    from insert_employees import insert_employees
    insert_employees(json_file_name="employees.json")
    return HttpResponse("Inserted employees")
