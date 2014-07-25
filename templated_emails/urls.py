from django.conf.urls import patterns, url

from .views import *


urlpatterns = patterns('',
    url(r'^$', index, name="templated_emails_index"),
    url(r'^view(?P<path>[\w.+-_/]+)$', view, name="templated_email_view"),
)
