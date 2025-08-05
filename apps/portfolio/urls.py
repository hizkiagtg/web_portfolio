from django.urls import path
from . import views

app_name = 'portfolio'

urlpatterns = [
    path('skills/', views.SkillListView.as_view(), name='skill_list'),
    path('projects/', views.ProjectListView.as_view(), name='project_list'),
    path('projects/<slug:slug>/', views.ProjectDetailView.as_view(), name='project_detail'),
    path('experience/', views.ExperienceListView.as_view(), name='experience_list'),
    path('personal-info/', views.personal_info, name='personal_info'),
]