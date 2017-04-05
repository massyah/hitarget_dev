from . import views
from django.conf.urls import url
from . import views

urlpatterns = [
    # post views
    url(r'^$', views.home, name='home'),
    url(r'blank', views.blank, name='blank'),
    url(r'add', views.add_lead, name='add_lead'),
    url(r'my-leads', views.my_leads, name='my-leads'),
    url(r'tips', views.tips, name='tips'),
    url(r'search_leads', views.search_leads, name='search_leads'),

    url(r'(?P<slug>[-\w]+?)/full$', views.lead_detail_full, name='lead_detail_full'),
    url(r'(?P<slug>[-\w]+?)/$', views.lead_detail, name='lead_detail'),
    url(r'(?P<slug>[-\w]+?)/edit$', views.lead_edit, name='lead_edit'),
    url(r'(?P<slug>[-\w]+?)/delete$', views.lead_delete, name='lead_delete'),
]
