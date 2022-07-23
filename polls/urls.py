from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.index, name='index'),
    # ex: /polls/5/
    path('<int:question_id>/', views.detail, name='detail'),
    # ex: /polls/5/results/
    path('results/<int:id>', views.results, name='results'),
    path('remarks/', views.remarks, name='remarks'),
    # ex: /polls/5/vote/
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('add_remark/', views.add_remark, name='add_remark'),
    path('add_student_name/', views.add_student_name, name='add_student_name'),
]