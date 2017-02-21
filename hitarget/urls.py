from . import views
from django.conf.urls import url
from . import views

urlpatterns = [
    # post views
    url(r'^$', views.home, name='home'),
    url(r'blank', views.blank, name='blank'),
    url(r'add', views.add_lead, name='add_lead'),
    url(r'tips', views.tips, name='tips'),
    url(r'(?P<slug>[-\w]+?)/full$',
        views.lead_detail_full,
        name='lead_detail_full'),

    url(r'(?P<slug>[-\w]+?)/$',
        views.lead_detail,
        name='lead_detail'),
]
