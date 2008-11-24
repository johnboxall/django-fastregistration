from django.conf.urls.defaults import *
from django.contrib.auth import views as auth_views
from django.views.generic.simple import direct_to_template

from fastregistration import views as fast_views


urlpatterns = patterns('',
    # register
    url(r'^register/$', fast_views.register,
        name='fast-register'),
    url(r'^register/done/$', direct_to_template, {'template': 'registration/register_done.html'},
        name='fast-register-done'),

    # forget password
    url(r'^password_request/$', auth_views.password_reset, {'template_name': 'registration/password_request.html'},
        name='fast-password-request'),
    url(r'^password_request/done/$', auth_views.password_reset_done, {'template_name': 'registration/password_request_done.html'},
        name='fast-password-request-done'),
    url(r'^password_reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', auth_views.password_reset_confirm, {'template_name': 'registration/password_reset.html'},
        name='fast-password-reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_complete, {'template_name': 'registration/password_reset_done.html'},
        name='fast-password-reset-done'),
        
    # manage profile email and password
    url(r'^profile/$', fast_views.profile,
        name='fast-profile'),
    url(r'^profile/email/update/$', fast_views.profile_email_update,
        name='fast-profile-email-update'),
    url(r'^profile/password/update/$', fast_views.profile_password_update,
        name='fast-profile-password-update'),
        
    # login logout
    url(r'^login/$', auth_views.login, {'template_name': 'registration/login.html'},
        name='fast-login'),
    url(r'^logout/$', auth_views.logout, {'template_name': 'registration/logout.html'},
        name='fast-logout'),
    url(r'^logout_then_login/$', auth_views.logout_then_login,
        name='fast-logout-then-login'),
    
)
