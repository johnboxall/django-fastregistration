from django.core import mail
from django.contrib.auth.models import User
from django.test import TestCase


class PasswordTestCase(TestCase):
    """
    Test for requesting forgotten password.
    """
    urls = 'fastregistration.urls'
    
    def setUp(self):
        self.user = User.objects.create_user('kegan@example.com', 'kegan@example.com', 'abcdefg')
        
        self.client.login(username='kegan@example.com', password='abcdefg')
    
    def test_get_request_password(self):
        """
        Get password request page.
        """
        response = self.client.get('/password_request/')
        self.assertTemplateUsed(response, 'registration/password_request.html')
    
    def test_post_request_password(self):
        """
        Request for forgotten password.
        """
        response = self.client.post('/password_request/', {'email': 'kegan@example.com'})
        self.assertRedirects(response, '/password_request/done/')
        self.assertEqual(len(mail.outbox), 1)
    
    def test_get_request_password_done(self):
        """
        Get done requesting password page.
        """
        response = self.client.get('/password_request/done/')
        self.assertTemplateUsed(response, 'registration/password_request_done.html')
    
    def test_get_reset_password(self):
        """
        Get reset password page.
        """
        response = self.client.post('/password_request/', {'email': 'kegan@example.com'})
        response = self.client.get('/password_reset/%s-%s/' % (response.context['uid'], response.context['token']))
        self.assertTemplateUsed(response, 'registration/password_reset.html')
    
    def test_post_reset_password(self):
        """
        Reset password.
        """
        response = self.client.post('/password_request/', {'email': 'kegan@example.com'})
        inputs = {
            'new_password1': '123456',
            'new_password2': '123456',
        }
        response = self.client.post('/password_reset/%s-%s/' % (response.context['uid'], response.context['token']), inputs)
        self.assertRedirects(response, '/password_reset/done/')
    
    def test_get_reset_password_done(self):
        """
        Get done reseting password page.
        """
        response = self.client.get('/password_reset/done/')
        self.assertTemplateUsed(response, 'registration/password_reset_done.html')
    
    def tearDown(self):
        pass