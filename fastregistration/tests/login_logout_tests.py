from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.test import TestCase


URL_PREFIX = '/account/'

class LoginLogoutTestCase(TestCase):
    """
    Test for login logout.
    """    
    def setUp(self):
        User.objects.create_user(username='kegan@example.com', email='kegan@example.com', password='abcdefg')

    def test_get_login(self):
        """
        Access login page.
        """
        response = self.client.get(URL_PREFIX + 'login/')
        self.assertTemplateUsed(response, 'registration/login.html')
        
    def tearDown(self):
        pass
