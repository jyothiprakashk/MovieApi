from django.urls import path
from django.conf.urls import url
from . import views
# from django.contrib.auth.views import password_reset
# from django.contrib.auth.views import PasswordResetView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('search', views.index,name='search'),
    path('',views.trending,name='trending'),
    path('trending',views.trending,name='trending'),
    path('cast/<int:id>/',views.cast,name='Cast'),
    path('movielist',views.movielist,name='movielist'),
    path('delete/<int:id>/',views.delete,name='delete'),
    path('signup',views.signup,name='signup'),
    path('account',views.account,name='account'),
    path('log',views.log,name='log'),
    path('logouts',views.logouts,name='logouts'), 
    path('password_reset/',
         auth_views.PasswordResetView.as_view(
             template_name='registration/password_reset.html',
             subject_template_name='registration/password_reset_subject.txt',
             email_template_name='registration/password_reset_email.html',
         )),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='registration/password_done.html')),
    # path('password_reset_confirm/<uidb64>/<token>/',
    #      auth_views.PasswordResetConfirmView.as_view(
    #          template_name='registration/password_reset_email.html'
    #      )),
    
    path('password_change/',
        auth_views.PasswordChangeView.as_view(),
    ),   
]

