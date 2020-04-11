from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import AnonymousUser

from .models import Company, Employee, Request, Review
from .views import homepage
# https://docs.djangoproject.com/en/3.0/topics/testing/tools/#django.test.TestCase

class TestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_homepage(self):
        breakpoint()
        request = self.factory.get('')
        request.user = AnonymousUser()
        response = homepage(request)
        self.assertEqual(response.status_code, 200)