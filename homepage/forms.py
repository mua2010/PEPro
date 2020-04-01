from django import forms
from django.core.exceptions import ValidationError
from .models import Employee, Request

class RequestReviewForm(forms.Form):
    reviewee_email = forms.EmailField(label="Your Email", max_length=100)
    reviewer_email = forms.EmailField(label="Co-Worker's Email", max_length=100)

    def clean(self):
        reviewee_email = self.cleaned_data["reviewee_email"]
        reviewer_email = self.cleaned_data["reviewer_email"]

        if not Employee.objects.filter(email=reviewee_email).exists():
            raise ValidationError("Your email does match any emails on record")

        if not Employee.objects.filter(email=reviewer_email).exists():
            raise ValidationError("Co-Worker's email does match any emails on record")

        reviewee = Employee.objects.get(email=reviewee_email)
        reviewer = Employee.objects.get(email=reviewer_email)
        if Request.objects.filter(request_reviewee=reviewee, request_reviewer=reviewer).exists():
            raise ValidationError("There is already a pending review request to this person")

        if reviewee_email == reviewer_email:
            raise ValidationError("You cannot review yourself")

        return self.cleaned_data


    def insert(self):
        '''
        Inserts this request object into the request table
        returns the new request object
        '''
        reviewee_email = self.cleaned_data["reviewee_email"]
        reviewer_email = self.cleaned_data["reviewer_email"]

        reviewee = Employee.objects.get(email=reviewee_email)
        reviewer = Employee.objects.get(email=reviewer_email)

        return Request.objects.create(request_reviewer=reviewer, request_reviewee=reviewee)
        