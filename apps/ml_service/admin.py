from django.contrib import admin
from .models import SpamClassification


@admin.register(SpamClassification)
class SpamClassificationAdmin(admin.ModelAdmin):
    list_display = ('text_input_short', 'prediction', 'confidence', 'created_at')
    list_filter = ('prediction', 'created_at')
    search_fields = ('text_input',)
    readonly_fields = ('created_at', 'updated_at')

    def text_input_short(self, obj):
        return obj.text_input[:50] + "..." if len(obj.text_input) > 50 else obj.text_input
    text_input_short.short_description = "Text Input"