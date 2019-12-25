from django.urls import path
from . import views
#handler404 = 'baseapi.views.my_custom_404_view'

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
    #path('handler404',views.handler404,name="handler404")
]

