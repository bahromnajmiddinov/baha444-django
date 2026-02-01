from django.urls import path
from . import views

urlpatterns = [
    path('', views.pomodoro_view, name='pomodoro'),
    path('start/', views.start_session, name='pomodoro_start'),
    path('<int:pk>/complete/', views.complete_session, name='pomodoro_complete'),
]
