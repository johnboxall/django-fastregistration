from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _


class RegistrationForm(forms.Form):
    """
    Registration form for new users.
    
    """
    email     = forms.EmailField(label=_("Email"), max_length=75)  # username max_length = 30
    password1 = forms.CharField(label=_("Password"), max_length=16, widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password Confirmation"), max_length=16, widget=forms.PasswordInput)
    
    def clean_email(self):
        email = self.cleaned_data.get("email")
        try:
            User.objects.get(username=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError(_("There is already a user with this email."))
    
    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_(u'You must type the same password each time'))                
        return self.cleaned_data

    # @@@ This business is really silly. No profile_cb - do that yourself with signals.
    # @@@ This should be made into a request form.
    def save(self, request, profile_cb=None):
        args = [self.cleaned_data["email"], self.cleaned_data["email"], self.cleaned_data["password1"]]
        user = User.objects.create_user(*args)
        
        if profile_cb is not None:
            profile_cb(user)
        
        # Return p/w so we can log the dude in.
        return user, self.cleaned_data["password1"]