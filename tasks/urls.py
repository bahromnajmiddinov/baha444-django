from django.urls import path
from . import views

urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('create/', views.task_create, name='task_create'),
    path('<int:pk>/', views.task_detail, name='task_detail'),
    path('<int:pk>/update/', views.task_update, name='task_update'),
    path('<int:pk>/delete/', views.task_delete, name='task_delete'),
    path('<int:pk>/status/', views.task_update_status, name='task_update_status'),
    path('<int:pk>/toggle-pin/', views.task_toggle_pin, name='task_toggle_pin'),
    path('<int:pk>/archive/', views.task_archive, name='task_archive'),
    path('<int:pk>/activity/', views.task_activity_log, name='task_activity_log'),
    path('calendar/', views.calendar_view, name='task_calendar'),
    path('tags/', views.tag_list, name='tag_list'),
    path('tags/create/', views.tag_create, name='tag_create'),
    path('tags/<int:pk>/', views.tag_detail, name='tag_detail'),
    path('tags/<int:pk>/update/', views.tag_update, name='tag_update'),
    path('tags/<int:pk>/delete/', views.tag_delete, name='tag_delete'),
    path('lists/', views.tasklist_list, name='tasklist_list'),
    path('lists/create/', views.tasklist_create, name='tasklist_create'),
    path('lists/<int:pk>/', views.tasklist_detail, name='tasklist_detail'),
    path('lists/<int:pk>/update/', views.tasklist_update, name='tasklist_update'),
    path('lists/<int:pk>/archive/', views.tasklist_archive, name='tasklist_archive'),
    path('dashboard/', views.dashboard_enhanced, name='dashboard_enhanced'),
]
