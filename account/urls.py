from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # post views
    # url(r'^login/$', views.user_login, name='login'),
    url(r'^login/$', auth_views.login, {'template_name': 'account/login.html'}, name='login'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^logout/$', auth_views.logout, {'template_name': 'account/logged_out.html'}, name='logout'),
    url(r'^logout-then-login/$', auth_views.logout_then_login, name='logout_then_login'),
    # change password urls
    url(r'^password-change/$', auth_views.password_change, {'template_name': 'account/password_change.html'}, name='password_change'),
    url(r'^password-change/done/$', auth_views.password_change_done, name='password_change_done'),
    # password reset by e-mail, cf django book for recipe

    # new user registration
    url(r'^register/$', views.register, name='register'),
    url(r'^edit/$', views.edit, name='edit')
]
