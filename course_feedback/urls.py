from django.contrib import admin
from django.urls import path,include
from django.contrib.auth import views
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('give_feedback/', views.give_feedback,name='give_feedback'),
    path('sort_courses/',views.sort_courses,name='sort_courses'),
    path('get_feedback/',views.get_feedback,name='get_feedback'),
    path('show_review/<int:pk>/',views.show_review,name='show_review'),
    path('signup/',views.signup,name='signup'),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
        views.activate, name='activate'),
    path('add_review/<int:pk>/',views.add_review,name='add_review'),
   

]
