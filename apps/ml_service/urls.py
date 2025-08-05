from django.urls import path
from . import views

app_name = 'ml_service'

urlpatterns = [
    path('classify/', views.classify_spam, name='classify_spam'),
    path('history/', views.classification_history, name='classification_history'),
    path('health/', views.health_check, name='health_check'),
]