from django.urls import re_path
from first_app import views

# For Template Tagging, Global Name
app_name = 'first_app'

urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    re_path(r'reg_user/', views.regUser, name='RegUser'),
    re_path(r'^relative/$', views.relative, name='relative'),
    re_path(r'^other/$', views.other, name='other'),
    re_path(r'^register/$', views.register, name='register'),
    re_path(r'^login/$', views.user_login, name='login')
]