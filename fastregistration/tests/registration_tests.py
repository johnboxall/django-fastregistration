from django.contrib.auth.models import User
from django.test import TestCase
from django.utils.translation import ugettext as _


URL_PREFIX = '/account/'

class RegistrationTestCase(TestCase):
    """
    Test for registration.
    """
    def setUp(self):
        pass
    
    def test_get_registration(self):
        response = self.client.get(URL_PREFIX + 'register/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/register.html')
    
    def test_simple_registration(self):
        """
        Straight forward registration.
        """
        inputs = {
            'email1': 'kegan@kegan.info',
            'email2': 'kegan@kegan.info',
            'password1': 'secret_password',
            'password2': 'secret_password',
        }
        response = self.client.post(URL_PREFIX + 'register/', inputs)
        self.assertRedirects(response, URL_PREFIX + 'register/done/')

        user = User.objects.get(email=inputs['email1'])
        self.assertEquals(user.username, inputs['email1'])
        self.assertEquals(user.email, inputs['email1'])
        
    def test_dissimilar_email(self):
        """
        Emails not consistent.
        """
        inputs = {
            'email1': 'kegan@kegan.info',
            'email2': 'another@another.info',
            'password1': 'secret_password',
            'password2': 'secret_password',
        }
        response = self.client.post(URL_PREFIX + 'register/', inputs)
        self.assertFormError(response, 'form', 'email2', _("The two email fields does not match."))
        self.assertTemplateUsed(response, 'registration/register.html')

    def test_dissimilar_password(self):
        """
        Emails not consistent.
        """
        inputs = {
            'email1': 'kegan@kegan.info',
            'email2': 'kegan@kegan.info',
            'password1': 'secret_password',
            'password2': 'another_password',
        }
        response = self.client.post(URL_PREFIX + 'register/', inputs)
        self.assertFormError(response, 'form', 'password2', _("The two password fields does not match."))
        self.assertTemplateUsed(response, 'registration/register.html')
        
    def test_email_existed(self):
        """
        Email used already existed in the system.
        """
        inputs = {
            'email1': 'kegan@kegan.info',
            'email2': 'kegan@kegan.info',
            'password1': 'secret_password',
            'password2': 'secret_password',
        }
        response = self.client.post(URL_PREFIX + 'register/', inputs)
        self.assertRedirects(response, URL_PREFIX + 'register/done/')

        user = User.objects.get(email=inputs['email1'])
        self.assertEquals(user.username, inputs['email1'])
        self.assertEquals(user.email, inputs['email1'])
        
        # register again
        response = self.client.post(URL_PREFIX + 'register/', inputs)
        self.assertFormError(response, 'form', 'email1', _("There is already a user with this email. You cannot use this email to register."))
        self.assertTemplateUsed(response, 'registration/register.html')
            
    def tearDown(self):
        pass
