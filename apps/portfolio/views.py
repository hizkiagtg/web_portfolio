from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from drf_spectacular.utils import extend_schema

from .models import Skill, Project, Experience, PersonalInfo
from .serializers import (
    SkillSerializer, ProjectListSerializer, ProjectDetailSerializer,
    ExperienceSerializer, PersonalInfoSerializer
)


@method_decorator(cache_page(60 * 15), name='dispatch')  # Cache for 15 minutes
class SkillListView(generics.ListAPIView):
    """List all skills"""
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [AllowAny]

    @extend_schema(
        summary="List all skills",
        description="Retrieve a list of all skills and technologies",
        tags=["Portfolio"]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.query_params.get('category')
        featured = self.request.query_params.get('featured')
        
        if category:
            queryset = queryset.filter(category=category)
        if featured and featured.lower() == 'true':
            queryset = queryset.filter(is_featured=True)
            
        return queryset


@method_decorator(cache_page(60 * 15), name='dispatch')
class ProjectListView(generics.ListAPIView):
    """List all published projects"""
    queryset = Project.objects.filter(is_published=True)
    serializer_class = ProjectListSerializer
    permission_classes = [AllowAny]

    @extend_schema(
        summary="List all projects",
        description="Retrieve a list of all published portfolio projects",
        tags=["Portfolio"]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        featured = self.request.query_params.get('featured')
        
        if featured and featured.lower() == 'true':
            queryset = queryset.filter(is_featured=True)
            
        return queryset


@method_decorator(cache_page(60 * 15), name='dispatch')
class ProjectDetailView(generics.RetrieveAPIView):
    """Project detail view"""
    queryset = Project.objects.filter(is_published=True)
    serializer_class = ProjectDetailSerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'

    @extend_schema(
        summary="Get project details",
        description="Retrieve detailed information about a specific project",
        tags=["Portfolio"]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


@method_decorator(cache_page(60 * 15), name='dispatch')
class ExperienceListView(generics.ListAPIView):
    """List all experiences"""
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer
    permission_classes = [AllowAny]

    @extend_schema(
        summary="List all experiences",
        description="Retrieve a list of work experience, education, and certifications",
        tags=["Portfolio"]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        experience_type = self.request.query_params.get('type')
        
        if experience_type:
            queryset = queryset.filter(experience_type=experience_type)
            
        return queryset


@extend_schema(
    summary="Get personal information",
    description="Retrieve personal information and contact details",
    responses={200: PersonalInfoSerializer},
    tags=["Portfolio"]
)
@api_view(['GET'])
@permission_classes([AllowAny])
@cache_page(60 * 30)  # Cache for 30 minutes
def personal_info(request):
    """Get personal information"""
    try:
        info = PersonalInfo.objects.first()
        if info:
            serializer = PersonalInfoSerializer(info)
            return Response(serializer.data)
        return Response(
            {"message": "Personal information not available"},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {"error": "Unable to retrieve personal information"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )