from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/new-game/', views.new_game, name='new_game'),
    path('api/fire/', views.fire, name='fire'),
]
