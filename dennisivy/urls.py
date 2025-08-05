"""dennisivy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

# Admin customization
admin.site.site_header = "Portfolio Admin"
admin.site.site_title = "Portfolio Admin Portal"
admin.site.index_title = "Welcome to Portfolio Administration"

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # Main website
    path('', include('apps.core.urls')),
    
    # API endpoints
    path('api/portfolio/', include('apps.portfolio.urls')),
    path('api/ml/', include('apps.ml_service.urls')),
    
    # API Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    # CKEditor
    path('ckeditor/', include('ckeditor_uploader.urls')),
    
    # Authentication (Password Reset)
    path('auth/password-reset/', 
         auth_views.PasswordResetView.as_view(
             template_name="auth/password_reset.html"
         ), 
         name="password_reset"),
    path('auth/password-reset-done/', 
         auth_views.PasswordResetDoneView.as_view(
             template_name="auth/password_reset_done.html"
         ),
         name="password_reset_done"),
    path('auth/reset/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(
             template_name="auth/password_reset_confirm.html"
         ), 
         name="password_reset_confirm"),
    path('auth/password-reset-complete/', 
         auth_views.PasswordResetCompleteView.as_view(
             template_name="auth/password_reset_complete.html"
         ), 
         name="password_reset_complete"),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
