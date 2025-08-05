from rest_framework import serializers
from .models import SpamClassification


class SpamClassificationRequestSerializer(serializers.Serializer):
    """Serializer for spam classification requests"""
    text = serializers.CharField(
        max_length=5000,
        help_text="Text to classify for spam detection"
    )


class SpamClassificationResponseSerializer(serializers.Serializer):
    """Serializer for spam classification responses"""
    prediction = serializers.CharField(help_text="Prediction result: spam or not_spam")
    confidence = serializers.FloatField(
        allow_null=True,
        help_text="Confidence score of the prediction (0-1)"
    )
    message = serializers.CharField(help_text="Human-readable prediction message")


class SpamClassificationSerializer(serializers.ModelSerializer):
    """Serializer for SpamClassification model"""
    
    class Meta:
        model = SpamClassification
        fields = [
            'id', 'text_input', 'prediction', 'confidence',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']