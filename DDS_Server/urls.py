from django.urls import path

from . import views

urlpatterns = [
    path('login', views.login, name='login'),
    path('signup', views.signup, name='signup'),
    path('report', views.report, name='report'),
    path('domainname_check', views.domainname_check, name='check'),
    path('predict', views.predict, name='predict'),
    path('subscribe', views.subscribe, name='subscribe'),
    path('user_update', views.user_update, name='user_update'),
]