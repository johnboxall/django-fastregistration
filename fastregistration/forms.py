from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _


class RegistrationForm(forms.Form):
    """
    Registration form for new users.
    """
    email1    = forms.EmailField(label=_("Email"), max_length=32)
    email2    = forms.EmailField(label=_("Email Confirmation"), max_length=32)
    password1 = forms.CharField(label=_("Password"), max_length=16, widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password Confirmation"), max_length=16, widget=forms.PasswordInput)
    
    def clean_email1(self):
        email1 = self.cleaned_data.get("email1")
        try:
            User.objects.get(username=email1)
        except User.DoesNotExist:
            return email1
        raise forms.ValidationError(_("There is already a user with this email. You cannot use this email to register."))
    
    def clean_email2(self):
        email1 = self.cleaned_data.get("email1")
        email2 = self.cleaned_data.get("email2")
        if email1 and email2 and (email1 != email2):
            raise forms.ValidationError(_("The two email fields does not match."))
        return email2
    
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and (password1 != password2):
            raise forms.ValidationError(_("The two password fields does not match."))
        return password2

class ProfileEmailForm(forms.Form):
    """
    Profile Email update form.
    """
    email1           = forms.EmailField(label=_("New Email"), max_length=32)
    email2           = forms.EmailField(label=_("Confirm New Email"), max_length=32)
    current_password = forms.CharField(label=_("Current Password"), max_length=16, widget=forms.PasswordInput)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(ProfileEmailForm, self).__init__(*args, **kwargs)
        
    def clean_email1(self):
        email1 = self.cleaned_data.get("email1")
        try:
            User.objects.get(username=email1)
        except User.DoesNotExist:
            return email1
        raise forms.ValidationError(_("There is already a user with this email. You cannot use this email to register."))
    
    def clean_email2(self):
        email1 = self.cleaned_data.get("email1")
        email2 = self.cleaned_data.get("email2")
        
        if email1 and email2 and (email1 != email2):
            raise forms.ValidationError(_("The two emails didn't match."))
        return email2

    def clean_current_password(self):
        current_password = self.cleaned_data.get("current_password")
        if not self.user.check_password(current_password):
            raise forms.ValidationError(_("The password is invalid."))
        return current_password

class ProfilePasswordForm(forms.Form):
    """
    Profile password update form.
    """
    password1        = forms.CharField(label=_("New Password"), max_length=16, widget=forms.PasswordInput)
    password2        = forms.CharField(label=_("Confirm New Password"), max_length=16, widget=forms.PasswordInput)
    current_password = forms.CharField(label=_("Current Password"), max_length=16, widget=forms.PasswordInput)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(ProfilePasswordForm, self).__init__(*args, **kwargs)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and (password1 != password2):
            raise forms.ValidationError(_("The two password fields didn't match."))
        return password2

    def clean_current_password(self):
        current_password = self.cleaned_data.get("current_password")
        if not self.user.check_password(current_password):
            raise forms.ValidationError(_("The password is invalid."))
        return current_password
