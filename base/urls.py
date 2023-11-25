from django.urls import path
from . import views

urlpatterns = [
	path('', views.home, name="home"),
	path('send_email/', views.sendEmail, name="send_email"),
    path('spam_classification/', views.spam_classification, name="spam_classification"),
    path('classify_sms/', views.classify_sms, name="classify_sms"),
]