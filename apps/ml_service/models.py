from django.db import models
from apps.core.models import TimeStampedModel


class SpamClassification(TimeStampedModel):
    """Model to track spam classification requests"""
    text_input = models.TextField()
    prediction = models.CharField(max_length=20, choices=[
        ('spam', 'Spam'),
        ('not_spam', 'Not Spam'),
    ])
    confidence = models.FloatField(blank=True, null=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.prediction} - {self.text_input[:50]}..."