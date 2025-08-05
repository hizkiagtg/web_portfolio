from rest_framework import serializers
from .models import Skill, Project, Experience, PersonalInfo


class SkillSerializer(serializers.ModelSerializer):
    """Serializer for Skill model"""
    
    class Meta:
        model = Skill
        fields = ['id', 'name', 'category', 'proficiency', 'icon', 'is_featured']


class ProjectListSerializer(serializers.ModelSerializer):
    """Serializer for Project list view"""
    technologies = SkillSerializer(many=True, read_only=True)
    
    class Meta:
        model = Project
        fields = [
            'id', 'title', 'slug', 'description', 'featured_image',
            'github_url', 'live_url', 'technologies', 'is_featured',
            'start_date', 'end_date', 'created_at'
        ]


class ProjectDetailSerializer(serializers.ModelSerializer):
    """Serializer for Project detail view"""
    technologies = SkillSerializer(many=True, read_only=True)
    
    class Meta:
        model = Project
        fields = [
            'id', 'title', 'slug', 'description', 'detailed_description',
            'github_url', 'live_url', 'technologies', 'featured_image',
            'gallery_images', 'is_featured', 'start_date', 'end_date',
            'created_at', 'updated_at'
        ]


class ExperienceSerializer(serializers.ModelSerializer):
    """Serializer for Experience model"""
    skills = SkillSerializer(many=True, read_only=True)
    
    class Meta:
        model = Experience
        fields = [
            'id', 'title', 'company_or_institution', 'location',
            'experience_type', 'description', 'start_date', 'end_date',
            'is_current', 'skills'
        ]


class PersonalInfoSerializer(serializers.ModelSerializer):
    """Serializer for Personal Information"""
    
    class Meta:
        model = PersonalInfo
        fields = [
            'id', 'name', 'title', 'bio', 'email', 'phone', 'location',
            'profile_image', 'resume', 'github_url', 'linkedin_url',
            'twitter_url', 'website_url'
        ]