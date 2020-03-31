from django.db import models

class Company(models.Model):
    company_id = models.IntegerField(default=None, primary_key=True)
    company_name = models.CharField(max_length=70)

    def __str__(self):
        return self.company_name

class Employee(models.Model):
    email = models.CharField(default=None, primary_key=True, max_length=70)
    employee_id = models.IntegerField()
    first_name = models.CharField(max_length=35)
    last_name = models.CharField(max_length=35)
    manager_id = models.IntegerField(blank=True, null=True)
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='company_id2company_id')

    def __str__(self):
        full_name = "%s %s" %(self.first_name, self.last_name)
        return full_name

class Review(models.Model):
    # The employee writing the review
    reviewer = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='reviewer2email', default=None)
    # The employee that requested to have a review written about them
    reviewee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='reviewee2email', default=None)
    review_text = models.CharField(max_length=10000, default=None)
    review_created_at = models.DateTimeField(default=None, blank=True)
    
    EDITING = 'E'
    SENT = 'S'
    
    STATUS_CHOICES = (
        (EDITING, 'editing'),
        (SENT, 'sent')
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=EDITING,
    )
    
    def __str__(self):
        return self.review_text

class Request(models.Model):
    request_created_at = models.DateTimeField(auto_now_add=True)
    # The employee writing the review
    reviewer = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='request_reviewer2email')
    # The employee that requested to have a review written about them
    reviewee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='request_reviewee2email')