from django.db import models
from django.urls import reverse
from apps.core.models import TimeStampedModel
from ckeditor.fields import RichTextField


class Skill(TimeStampedModel):
    """Model for skills/technologies"""
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=[
        ('frontend', 'Frontend'),
        ('backend', 'Backend'),
        ('database', 'Database'),
        ('devops', 'DevOps'),
        ('mobile', 'Mobile'),
        ('other', 'Other'),
    ])
    proficiency = models.IntegerField(choices=[
        (1, 'Beginner'),
        (2, 'Intermediate'),
        (3, 'Advanced'),
        (4, 'Expert'),
    ])
    icon = models.CharField(max_length=100, blank=True, help_text="CSS class for icon")
    is_featured = models.BooleanField(default=False)

    class Meta:
        ordering = ['-proficiency', 'name']

    def __str__(self):
        return self.name


class Project(TimeStampedModel):
    """Model for portfolio projects"""
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    detailed_description = RichTextField(blank=True)
    
    # Project links
    github_url = models.URLField(blank=True)
    live_url = models.URLField(blank=True)
    
    # Project details
    technologies = models.ManyToManyField(Skill, blank=True)
    featured_image = models.ImageField(upload_to='projects/', blank=True)
    gallery_images = models.JSONField(default=list, blank=True)
    
    # Project meta
    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    
    class Meta:
        ordering = ['-is_featured', '-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('portfolio:project_detail', kwargs={'slug': self.slug})


class Experience(TimeStampedModel):
    """Model for work/education experience"""
    EXPERIENCE_TYPES = [
        ('work', 'Work Experience'),
        ('education', 'Education'),
        ('volunteer', 'Volunteer'),
        ('certification', 'Certification'),
    ]
    
    title = models.CharField(max_length=200)
    company_or_institution = models.CharField(max_length=200)
    location = models.CharField(max_length=100, blank=True)
    experience_type = models.CharField(max_length=20, choices=EXPERIENCE_TYPES)
    description = RichTextField()
    
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    is_current = models.BooleanField(default=False)
    
    skills = models.ManyToManyField(Skill, blank=True)
    
    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.title} at {self.company_or_institution}"


class PersonalInfo(models.Model):
    """Model for personal information (singleton)"""
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    bio = RichTextField()
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=100)
    
    # Profile images
    profile_image = models.ImageField(upload_to='profile/', blank=True)
    resume = models.FileField(upload_to='resume/', blank=True)
    
    # Social links
    github_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    website_url = models.URLField(blank=True)
    
    class Meta:
        verbose_name = "Personal Information"
        verbose_name_plural = "Personal Information"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        if not self.pk and PersonalInfo.objects.exists():
            raise ValueError("Only one PersonalInfo instance is allowed")
        super().save(*args, **kwargs)