from django import forms
from .models import Employee, Request

class RequestReviewForm(forms.Form):
    your_first_name = forms.CharField(label="Your First Name", max_length=35)
    your_last_name = forms.CharField(label="Your Last Name", max_length=35)
    coworker_first_name = forms.CharField(label="Co-Worker First Name", max_length=35)
    coworker_last_name = forms.CharField(label="Co-Worker Last Name", max_length=35)

    def insert(self):
        data = self.cleaned_data
        author_first_name = data["coworker_first_name"]
        author_last_name = data["coworker_last_name"]
        recipient_first_name = data["your_first_name"]
        recipient_last_name = data["your_last_name"]
        authored_by = Employee.objects.get(first_name=author_first_name, last_name=author_last_name)
        recipient = Employee.objects.get(first_name=recipient_first_name, last_name=recipient_last_name)

        Request.objects.create(request_reviewer=authored_by, request_reviewee=recipient)

        