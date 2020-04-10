from django.urls import path
from . import views	

urlpatterns = [
    path('', views.index),
    path('users', views.createUser),
    path('login', views.login),
    path('homepage', views.homepage),
    path('logout', views.logout),
    path('postMessage', views.postMessage),
    path('postComment/<int:id>', views.postComment),
    path('deleteMessage/<int:id>', views.deleteMessage),
    path('deleteComment/<int:id>', views.deleteComment),
]