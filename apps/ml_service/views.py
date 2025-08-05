import logging
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from drf_spectacular.utils import extend_schema, OpenApiParameter

from .services import spam_classifier
from .models import SpamClassification
from .serializers import (
    SpamClassificationRequestSerializer,
    SpamClassificationResponseSerializer,
    SpamClassificationSerializer
)

logger = logging.getLogger(__name__)


@extend_schema(
    summary="Classify text for spam detection",
    description="Submit text to be classified as spam or not spam using machine learning",
    request=SpamClassificationRequestSerializer,
    responses={
        200: SpamClassificationResponseSerializer,
        400: {"description": "Bad request"},
        429: {"description": "Rate limit exceeded"},
        503: {"description": "Service unavailable - ML model not loaded"}
    },
    tags=["ML Service"]
)
@api_view(['POST'])
@permission_classes([AllowAny])
@ratelimit(key='ip', rate='30/m', method='POST')
def classify_spam(request):
    """
    Classify text as spam or not spam using machine learning
    """
    try:
        # Check if model is loaded
        if not spam_classifier.is_model_loaded():
            return Response(
                {"error": "ML model is not loaded. Please try again later."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        
        # Validate input
        serializer = SpamClassificationRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        text = serializer.validated_data['text']
        
        # Get client info
        ip_address = request.META.get('REMOTE_ADDR')
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        
        # Make prediction
        result = spam_classifier.predict(text)
        
        # Save to database for analytics
        try:
            SpamClassification.objects.create(
                text_input=text,
                prediction=result.get('prediction', 'unknown'),
                confidence=result.get('confidence'),
                ip_address=ip_address,
                user_agent=user_agent
            )
        except Exception as e:
            logger.warning(f"Failed to save classification to database: {e}")
        
        # Return response
        response_serializer = SpamClassificationResponseSerializer(data=result)
        if response_serializer.is_valid():
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        
        return Response(result, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Error in spam classification: {e}")
        return Response(
            {"error": "Internal server error"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@extend_schema(
    summary="Get classification history",
    description="Retrieve recent spam classification history (limited view)",
    responses={200: SpamClassificationSerializer(many=True)},
    tags=["ML Service"]
)
@api_view(['GET'])
@permission_classes([AllowAny])
@cache_page(60 * 5)  # Cache for 5 minutes
def classification_history(request):
    """
    Get recent classification history (anonymized)
    """
    try:
        # Get recent classifications (limit to protect privacy)
        recent_classifications = SpamClassification.objects.filter(
            text_input__isnull=False
        ).exclude(
            text_input__exact=''
        )[:50]
        
        # Anonymize data for public view
        anonymized_data = []
        for classification in recent_classifications:
            anonymized_data.append({
                'id': classification.id,
                'text_input': classification.text_input[:100] + "..." if len(classification.text_input) > 100 else classification.text_input,
                'prediction': classification.prediction,
                'confidence': classification.confidence,
                'created_at': classification.created_at,
            })
        
        return Response(anonymized_data, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Error retrieving classification history: {e}")
        return Response(
            {"error": "Unable to retrieve history"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@extend_schema(
    summary="ML Service health check",
    description="Check if the ML service is running and model is loaded",
    responses={
        200: {"description": "Service is healthy"},
        503: {"description": "Service is unavailable"}
    },
    tags=["ML Service"]
)
@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """
    Health check endpoint for ML service
    """
    is_healthy = spam_classifier.is_model_loaded()
    
    response_data = {
        'status': 'healthy' if is_healthy else 'unhealthy',
        'model_loaded': is_healthy,
        'service': 'ML Spam Classification Service'
    }
    
    status_code = status.HTTP_200_OK if is_healthy else status.HTTP_503_SERVICE_UNAVAILABLE
    
    return Response(response_data, status=status_code)