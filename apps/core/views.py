from django.shortcuts import render
from django.contrib import messages
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django_ratelimit.decorators import ratelimit
from drf_spectacular.utils import extend_schema

from apps.portfolio.models import PersonalInfo, Project, Skill, Experience
from .models import ContactMessage
import logging

logger = logging.getLogger(__name__)


def home(request):
    """Main portfolio homepage"""
    try:
        # Get personal info
        personal_info = PersonalInfo.objects.first()
        
        # Get featured projects
        featured_projects = Project.objects.filter(
            is_published=True, 
            is_featured=True
        )[:6]
        
        # Get featured skills
        featured_skills = Skill.objects.filter(is_featured=True)
        
        # Get recent experience
        recent_experience = Experience.objects.filter(
            experience_type='work'
        )[:3]
        
        context = {
            'personal_info': personal_info,
            'featured_projects': featured_projects,
            'featured_skills': featured_skills,
            'recent_experience': recent_experience,
        }
        
        return render(request, 'core/index.html', context)
        
    except Exception as e:
        logger.error(f"Error in home view: {e}")
        return render(request, 'core/index.html', {})


@extend_schema(
    summary="Send contact message",
    description="Submit a contact form message",
    request={
        'application/json': {
            'type': 'object',
            'properties': {
                'name': {'type': 'string'},
                'email': {'type': 'string', 'format': 'email'},
                'subject': {'type': 'string'},
                'message': {'type': 'string'}
            },
            'required': ['name', 'email', 'subject', 'message']
        }
    },
    responses={
        200: {'description': 'Message sent successfully'},
        400: {'description': 'Invalid data'},
        429: {'description': 'Rate limit exceeded'}
    },
    tags=["Contact"]
)
@api_view(['POST'])
@permission_classes([AllowAny])
@ratelimit(key='ip', rate='5/m', method='POST')
def send_contact_message(request):
    """Handle contact form submissions"""
    try:
        # Get form data
        name = request.data.get('name', '').strip()
        email = request.data.get('email', '').strip()
        subject = request.data.get('subject', '').strip()
        message = request.data.get('message', '').strip()
        
        # Validate required fields
        if not all([name, email, subject, message]):
            return Response(
                {'error': 'All fields are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Basic email validation
        if '@' not in email or '.' not in email:
            return Response(
                {'error': 'Please provide a valid email address'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Save to database
        contact_message = ContactMessage.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
        )
        
        # Send email notification
        try:
            email_template = render_to_string('core/email_template.html', {
                'name': name,
                'email': email,
                'subject': subject,
                'message': message,
            })
            
            email_message = EmailMessage(
                f'Portfolio Contact: {subject}',
                email_template,
                settings.EMAIL_HOST_USER,
                [settings.EMAIL_HOST_USER]  # Send to yourself
            )
            
            email_message.content_subtype = 'html'
            email_message.send(fail_silently=False)
            
        except Exception as e:
            logger.warning(f"Failed to send email notification: {e}")
            # Don't fail the request if email fails
        
        return Response(
            {'message': 'Thank you for your message! I will get back to you soon.'},
            status=status.HTTP_200_OK
        )
        
    except Exception as e:
        logger.error(f"Error in contact form: {e}")
        return Response(
            {'error': 'Unable to send message. Please try again later.'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )