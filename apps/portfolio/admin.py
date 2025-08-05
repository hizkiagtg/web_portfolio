from django.contrib import admin
from .models import Skill, Project, Experience, PersonalInfo


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'proficiency', 'is_featured')
    list_filter = ('category', 'proficiency', 'is_featured')
    search_fields = ('name',)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_featured', 'is_published', 'created_at')
    list_filter = ('is_featured', 'is_published', 'technologies')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('technologies',)


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('title', 'company_or_institution', 'experience_type', 'start_date', 'is_current')
    list_filter = ('experience_type', 'is_current')
    search_fields = ('title', 'company_or_institution')
    filter_horizontal = ('skills',)


@admin.register(PersonalInfo)
class PersonalInfoAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        # Only allow adding if no instance exists
        return not PersonalInfo.objects.exists()

    def has_delete_permission(self, request, obj=None):
        # Don't allow deletion
        return False