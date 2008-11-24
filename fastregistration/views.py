from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext as _
    
from forms import *


def register(request, success_url=None, form_class=RegistrationForm,
            profile_callback=None,
            template_name='registration/register.html'):
    """
    Register new users.
    """
    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            # Create the user instance.
            user = User.objects.create_user(form.cleaned_data["email1"], form.cleaned_data["email1"], form.cleaned_data["password1"])
            
            if profile_callback is not None:
                profile_callback(user)
            
            # Login.
            user = auth.authenticate(username=user.username, password=form.cleaned_data["password1"])
            auth.login(request, user)
            
            # Show and let user edit profile upon registration.
            return HttpResponseRedirect(success_url or reverse('fast-register-done'))
    elif request.method == 'GET':
        form = form_class()
    else:
        return HttpResponseRedirect(request.path)
    
    context = RequestContext(request, {
        'form': form
    })
    return render_to_response(template_name, context)
    
@login_required
def profile(request, template_name='registration/profile.html'):
    """
    Display user profile information.
    """
    if request.method == 'GET':
        pass
    else:
        return HttpResponseRedirect(reverse('fast-profile'))
        
    context = RequestContext(request)
    return render_to_response(template_name, context)
    
@login_required
def profile_email_update(request, form_class=ProfileEmailForm,
            success_message=_('Your email has been successfully updated.'),
            template_name='registration/profile_email_update.html'):
    """
    Update user profile email.
    """
    if request.method == 'POST':
        form = form_class(request.user, request.POST)
        if form.is_valid():
            request.user.username = form.cleaned_data['email1']
            request.user.email = form.cleaned_data['email1']
            request.user.save()
            request.user.message_set.create(message=success_message)
            return HttpResponseRedirect(reverse('fast-profile'))
    elif request.method == 'GET':
        form = form_class(request.user)
    else:
        return HttpResponseRedirect(request.path)

    context = RequestContext(request, {
        'form': form
    })
    return render_to_response(template_name, context)

@login_required
def profile_password_update(request, form_class=ProfilePasswordForm,
            success_message=_('Your password has been successfully updated.'),
            template_name='registration/profile_password_update.html'):
    """
    Update user profile password.
    """
    if request.method == 'POST':
        form = form_class(request.user, request.POST)
        if form.is_valid():
            request.user.set_password(form.cleaned_data['password1'])
            request.user.save()
            request.user.message_set.create(message=success_message)
            return HttpResponseRedirect(reverse('fast-profile'))
    elif request.method == 'GET':
        form = form_class(request.user)
    else:
        return HttpResponseRedirect(request.path)

    context = RequestContext(request, {
        'form': form
    })
    return render_to_response(template_name, context)
