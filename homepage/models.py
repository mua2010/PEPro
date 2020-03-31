from django.db import models

class Company(models.Model):
    company_id = models.IntegerField(default=None, primary_key=True)
    company_name = models.CharField(max_length=70)

    def __str__(self):
        return self.company_name

class Employee(models.Model):
    auto_increment_id = models.AutoField(primary_key=True)
    employee_id = models.IntegerField()
    first_name = models.CharField(max_length=35)
    last_name = models.CharField(max_length=35)
    manager_id = models.IntegerField(blank=True, null=True)
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='company_id2company_id')
    email = models.CharField(max_length=70)

    def __str__(self):
        full_name = "%s %s" %(self.first_name, self.last_name)
        return full_name

class Review(models.Model):
    # reviewer: The employee writing the review
    reviewer = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='reviewer2employee_id', default=None)
    # reviewee: The employee that requested to have a review written about them
    reviewee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='reviewee2employee_id', default=None)
    review_text = models.CharField(max_length=10000, default=None)
    review_requested_at = models.DateTimeField(auto_now_add=True)
    review_edited_at = models.DateTimeField(auto_now=True, blank=True)
    
    # P => accpeted or declined?
    PENDING = 'P'
    EDITING = 'E'
    SENT = 'S'
    
    STATUS_CHOICES = (
        (PENDING, 'pending'),
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