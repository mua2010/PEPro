from django.db import models

import datetime

class Company(models.Model):
    company_id = models.IntegerField(default=None, primary_key=True)
    company_name = models.CharField(max_length=100)

    def __str__(self):
        return self.company_name

class Employee(models.Model):
    employee_id = models.IntegerField(default=None, primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    manager_id = models.IntegerField()
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='company_id2company_id')

    def __str__(self):
        full_name = "%s %s" %(self.first_name, self.last_name)
        return full_name

class Review(models.Model):
    authored_by = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='authored_by2employee_id')
    recipient = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='recipient2employee_id')
    review_text = models.CharField(max_length=10000)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    requested_at = models.DateTimeField(auto_now_add=True, blank=True)
    
    EDITING = 'E'
    SENT = 'S'
    STATUS_CHOICES = (
        (EDITING, 'editing'),
        (SENT, 'sent'),
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=EDITING,
    )
    
    def __str__(self):
        return self.review_text