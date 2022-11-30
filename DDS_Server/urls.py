from django.urls import path

from . import views

urlpatterns = [
    path('login', views.login, name='login'),
    path('signup', views.signup, name='signup'),
    path('report', views.report, name='report'),
    path('url_check', views.url_check, name='check'),
    path('predict', views.predict, name='predict'),
    path('add_website', views.add_website, name='add_website'),
    path('add_contains', views.add_contains, name='add_contains')
]