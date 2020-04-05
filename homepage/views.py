from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404

from .forms import RequestReviewForm, GiveReviewForm
from .models import Review, Request, Employee



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
    form = GiveReviewForm(initial={"review_text":review.review_text})
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
