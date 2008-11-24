from django.core import mail
from django.contrib.auth.models import User
from django.test import TestCase
from django.utils.translation import ugettext as _


URL_PREFIX = '/account/'

class ProfileTestCase(TestCase):
    """
    Test for managing profile information.
    """        
    def setUp(self):
        self.user = User.objects.create_user('kegan@example.com', 'kegan@example.com', 'abcdefg')
        self.client.login(username='kegan@example.com', password='abcdefg')

        self.user2 = User.objects.create_user('kegan2@example.com', 'kegan2@example.com', 'abcdefg')
    
    def test_get_profile(self):
        """
        Get profile page.
        """
        response = self.client.get(URL_PREFIX + 'profile/')
        self.assertTemplateUsed(response, 'registration/profile.html')
    
    def test_get_profile_email_update(self):
        """
        Access profile email update page.
        """
        response = self.client.get(URL_PREFIX + 'profile/email/update/')
        self.assertTemplateUsed(response, 'registration/profile_email_update.html')
    
    def test_update_profile_email(self):
        """
        Update the profile email.
        """
        inputs = {
            'email1': 'new_email@example.com',
            'email2': 'new_email@example.com',
            'current_password': 'abcdefg',
        }
        response = self.client.post(URL_PREFIX + 'profile/email/update/', inputs)

        self.user = User.objects.get(pk=self.user.id)
        self.assertEquals(self.user.get_and_delete_messages()[0], _('Your email has been successfully updated.'))
        self.assertTrue(self.user.email == inputs['email1'])
        self.assertRedirects(response, URL_PREFIX + 'profile/')
    
    def test_update_profile_email_dissimilar_email(self):
        """
        Update profile email with dissimilar email.
        """
        inputs = {
            'email1': 'new_emailxxx@example.com',
            'email2': 'new_emailyyy@example.com',
            'current_password': 'abcdefg',
        }
        response = self.client.post(URL_PREFIX + 'profile/email/update/', inputs)
        self.assertTemplateUsed(response, 'registration/profile_email_update.html')
        self.assertFormError(response, 'form', 'email2', "The two emails didn't match.")
        
        user = User.objects.get(pk=self.user.id)
        self.assertTrue(user.email == 'kegan@example.com')
        
    def test_update_profile_email_existing(self):
        """
        Update profile email with existing email by another user.
        """
        inputs = {
            'email1': 'kegan2@example.com',
            'email2': 'kegan2@example.com',
            'current_password': 'abcdefg',
        }
        response = self.client.post(URL_PREFIX + 'profile/email/update/', inputs)
        self.assertTemplateUsed(response, 'registration/profile_email_update.html')
        self.assertFormError(response, 'form', 'email1', "There is already a user with this email. You cannot use this email to register.")
        
        user = User.objects.get(pk=self.user.id)
        self.assertTrue(user.email == 'kegan@example.com')
    
    def test_update_profile_email_invalid_password(self):
        """
        Update profile email with invalid current password.
        """
        inputs = {
            'email1': 'new_email@example.com',
            'email2': 'new_email@example.com',
            'current_password': 'xxxxxx-invalid',
        }
        response = self.client.post(URL_PREFIX + 'profile/email/update/', inputs)
        self.assertTemplateUsed(response, 'registration/profile_email_update.html')
        self.assertFormError(response, 'form', 'current_password', "The password is invalid.")
        
        user = User.objects.get(pk=self.user.id)
        self.assertTrue(user.email == 'kegan@example.com')
    
    def test_get_profile_password_update(self):
        """
        Access profile password update page.
        """
        response = self.client.get(URL_PREFIX + 'profile/password/update/')
        self.assertTemplateUsed(response, 'registration/profile_password_update.html')
    
    def test_update_profile_password(self):
        """
        Update the profile password.
        """
        inputs = {
            'password1': '123456',
            'password2': '123456',
            'current_password': 'abcdefg',
        }
        response = self.client.post(URL_PREFIX + 'profile/password/update/', inputs)
        
        self.user = User.objects.get(pk=self.user.id)
        self.assertEquals(self.user.get_and_delete_messages()[0], _('Your password has been successfully updated.'))
        self.assertTrue(self.user.check_password('123456'))
        self.assertRedirects(response, URL_PREFIX + 'profile/')
    
    def test_update_profile_password_dissimilar_password(self):
        """
        Update profile password with dissimilar password.
        """
        inputs = {
            'password1': 'xxxxxx',
            'password2': 'yyyyyy',
            'current_password': 'abcdefg',
        }
        response = self.client.post(URL_PREFIX + 'profile/password/update/', inputs)
        self.assertTemplateUsed(response, 'registration/profile_password_update.html')
        self.assertFormError(response, 'form', 'password2', "The two password fields didn't match.")
        
        user = User.objects.get(pk=self.user.id)
        self.assertTrue(user.check_password('abcdefg'))
    
    def test_update_profile_passwprd_invalid_password(self):
        """
        Update profile password with invalid current password.
        """
        inputs = {
            'password1': 'newpassword',
            'password2': 'newpassword',
            'current_password': 'invalid-current',
        }
        response = self.client.post(URL_PREFIX + 'profile/password/update/', inputs)
        self.assertTemplateUsed(response, 'registration/profile_password_update.html')
        self.assertFormError(response, 'form', 'current_password', "The password is invalid.")
        
        user = User.objects.get(pk=self.user.id)
        self.assertTrue(user.check_password('abcdefg'))
    
    def tearDown(self):
        pass