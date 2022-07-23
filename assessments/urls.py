from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'assessments'

urlpatterns = [
   # post views
   path('', views.dashboard, name='dashboard'),
   path('new/', views.new, name='new'),
   path('notifications/', views.notifications, name='notifications'),
   path('detail/<int:id>', views.detail, name='detail'),
   path('get_messages/', views.get_messages, name='get_messages'),
   path('send_message/', views.send_message, name='send_message'),
   path('add_student/', views.add_student, name='add_student'),
   path('add_wrl_supervisor/', views.add_wrl_supervisor, name='add_wrl_supervisor'),
   path('student_detail/<int:id>', views.student_detail, name='student_detail'),
   path('update_prog/', views.update_prog, name='update_prog'),
   path('approve/<int:id>', views.approve, name='approve'),


]