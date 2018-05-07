from django.conf.urls import url

from . import views

app_name = 'tree'
urlpatterns = [
    url(r'^tree/(?P<name>\w+)/$', views.TreeView.as_view()),
    url(r'^ajax/tree/$', views.TreeUpdateView.as_view()),
]
