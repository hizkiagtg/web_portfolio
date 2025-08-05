import json
from unittest.mock import patch, MagicMock
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import SpamClassification
from .services import SpamClassificationService


class SpamClassificationModelTestCase(TestCase):
    """Test cases for SpamClassification model"""
    
    def test_spam_classification_creation(self):
        """Test creating a spam classification record"""
        classification = SpamClassification.objects.create(
            text_input="This is a test message",
            prediction="not_spam",
            confidence=0.85,
            ip_address="127.0.0.1",
            user_agent="Test User Agent"
        )
        
        self.assertEqual(str(classification), "not_spam - This is a test message...")
        self.assertEqual(classification.prediction, "not_spam")
        self.assertEqual(classification.confidence, 0.85)
        self.assertIsNotNone(classification.created_at)
    
    def test_spam_classification_ordering(self):
        """Test spam classification ordering"""
        classification1 = SpamClassification.objects.create(
            text_input="First message",
            prediction="spam"
        )
        
        classification2 = SpamClassification.objects.create(
            text_input="Second message",
            prediction="not_spam"
        )
        
        # Check ordering (newest first)
        classifications = list(SpamClassification.objects.all())
        self.assertEqual(classifications[0], classification2)
        self.assertEqual(classifications[1], classification1)
    
    def test_long_text_truncation_in_str(self):
        """Test string representation truncates long text"""
        long_text = "A" * 100
        classification = SpamClassification.objects.create(
            text_input=long_text,
            prediction="spam"
        )
        
        str_repr = str(classification)
        self.assertTrue(str_repr.endswith("..."))
        self.assertLess(len(str_repr), len(long_text) + 20)


class SpamClassificationServiceTestCase(TestCase):
    """Test cases for SpamClassificationService"""
    
    def setUp(self):
        self.service = SpamClassificationService()
    
    @patch('apps.ml_service.services.pickle.load')
    @patch('builtins.open')
    @patch('pathlib.Path.exists')
    def test_model_loading_success(self, mock_exists, mock_open, mock_pickle_load):
        """Test successful model loading"""
        mock_exists.return_value = True
        mock_model = MagicMock()
        mock_vectorizer_data = ['test', 'data']
        mock_pickle_load.side_effect = [mock_model, mock_vectorizer_data]
        
        service = SpamClassificationService()
        
        self.assertIsNotNone(service.model)
        self.assertIsNotNone(service.X_train)
    
    @patch('pathlib.Path.exists')
    def test_model_loading_failure(self, mock_exists):
        """Test model loading when files don't exist"""
        mock_exists.return_value = False
        
        service = SpamClassificationService()
        
        self.assertIsNone(service.model)
        self.assertIsNone(service.X_train)
    
    def test_preprocessing_function(self):
        """Test text preprocessing function"""
        test_text = "This is a test message with some words!"
        result = self.service._preprocessing(test_text)
        
        self.assertIsInstance(result, list)
        # Should return lowercase, stemmed words without stopwords
        if result:  # Only test if preprocessing works (depends on installed packages)
            self.assertTrue(all(isinstance(word, str) for word in result))
    
    def test_is_model_loaded_false(self):
        """Test is_model_loaded returns False when model not loaded"""
        service = SpamClassificationService()
        service.model = None
        service.vectorizer = None
        
        self.assertFalse(service.is_model_loaded())
    
    @patch('apps.ml_service.services.SpamClassificationService._load_model')
    def test_is_model_loaded_true(self, mock_load_model):
        """Test is_model_loaded returns True when model loaded"""
        service = SpamClassificationService()
        service.model = MagicMock()
        service.vectorizer = MagicMock()
        
        self.assertTrue(service.is_model_loaded())
    
    def test_predict_no_model(self):
        """Test prediction when model is not loaded"""
        service = SpamClassificationService()
        service.model = None
        service.vectorizer = None
        
        result = service.predict("test message")
        
        self.assertEqual(result['prediction'], 'unknown')
        self.assertEqual(result['confidence'], 0.0)
        self.assertIn('error', result)
    
    @patch('apps.ml_service.services.SpamClassificationService.is_model_loaded')
    def test_predict_with_mock_model(self, mock_is_loaded):
        """Test prediction with mocked model"""
        mock_is_loaded.return_value = True
        
        # Mock the model and vectorizer
        mock_model = MagicMock()
        mock_model.predict.return_value = [1]  # Spam
        
        mock_vectorizer = MagicMock()
        mock_vectorizer.transform.return_value = MagicMock()
        
        service = SpamClassificationService()
        service.model = mock_model
        service.vectorizer = mock_vectorizer
        
        result = service.predict("test spam message")
        
        self.assertEqual(result['prediction'], 'spam')
        self.assertIn('message', result)


class SpamClassificationAPITestCase(APITestCase):
    """Test cases for spam classification API endpoints"""
    
    def setUp(self):
        self.classify_url = reverse('ml_service:classify_spam')
        self.history_url = reverse('ml_service:classification_history')
        self.health_url = reverse('ml_service:health_check')
    
    @patch('apps.ml_service.views.spam_classifier.is_model_loaded')
    @patch('apps.ml_service.views.spam_classifier.predict')
    def test_classify_spam_success(self, mock_predict, mock_is_loaded):
        """Test successful spam classification"""
        mock_is_loaded.return_value = True
        mock_predict.return_value = {
            'prediction': 'spam',
            'confidence': 0.95,
            'message': 'This message is SPAM'
        }
        
        data = {'text': 'Buy now! Limited time offer!'}
        response = self.client.post(
            self.classify_url,
            data=json.dumps(data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(response_data['prediction'], 'spam')
        self.assertEqual(response_data['confidence'], 0.95)
        
        # Check if classification was saved to database
        self.assertTrue(SpamClassification.objects.filter(
            text_input=data['text']
        ).exists())
    
    @patch('apps.ml_service.views.spam_classifier.is_model_loaded')
    def test_classify_spam_model_not_loaded(self, mock_is_loaded):
        """Test spam classification when model is not loaded"""
        mock_is_loaded.return_value = False
        
        data = {'text': 'Test message'}
        response = self.client.post(
            self.classify_url,
            data=json.dumps(data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_503_SERVICE_UNAVAILABLE)
        self.assertIn('error', response.json())
    
    def test_classify_spam_invalid_data(self):
        """Test spam classification with invalid data"""
        data = {}  # Missing 'text' field
        response = self.client.post(
            self.classify_url,
            data=json.dumps(data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_classify_spam_method_not_allowed(self):
        """Test that GET method is not allowed for classification"""
        response = self.client.get(self.classify_url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def test_classification_history(self):
        """Test classification history endpoint"""
        # Create test classifications
        SpamClassification.objects.create(
            text_input="Test message 1",
            prediction="spam",
            confidence=0.8
        )
        
        SpamClassification.objects.create(
            text_input="Test message 2",
            prediction="not_spam",
            confidence=0.9
        )
        
        response = self.client.get(self.history_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertIsInstance(response_data, list)
        self.assertEqual(len(response_data), 2)
    
    def test_classification_history_anonymization(self):
        """Test that classification history is properly anonymized"""
        long_text = "A" * 150  # Text longer than 100 characters
        SpamClassification.objects.create(
            text_input=long_text,
            prediction="spam",
            confidence=0.8
        )
        
        response = self.client.get(self.history_url)
        response_data = response.json()
        
        # Check that long text is truncated
        if response_data:
            text_input = response_data[0]['text_input']
            self.assertTrue(text_input.endswith("..."))
            self.assertLessEqual(len(text_input), 103)  # 100 chars + "..."
    
    @patch('apps.ml_service.views.spam_classifier.is_model_loaded')
    def test_health_check_healthy(self, mock_is_loaded):
        """Test health check when service is healthy"""
        mock_is_loaded.return_value = True
        
        response = self.client.get(self.health_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(response_data['status'], 'healthy')
        self.assertTrue(response_data['model_loaded'])
    
    @patch('apps.ml_service.views.spam_classifier.is_model_loaded')
    def test_health_check_unhealthy(self, mock_is_loaded):
        """Test health check when service is unhealthy"""
        mock_is_loaded.return_value = False
        
        response = self.client.get(self.health_url)
        
        self.assertEqual(response.status_code, status.HTTP_503_SERVICE_UNAVAILABLE)
        response_data = response.json()
        self.assertEqual(response_data['status'], 'unhealthy')
        self.assertFalse(response_data['model_loaded'])


class MLServiceURLsTestCase(TestCase):
    """Test ML service URL routing"""
    
    def test_classify_url_resolves(self):
        """Test classify URL resolves correctly"""
        url = reverse('ml_service:classify_spam')
        self.assertEqual(url, '/api/ml/classify/')
    
    def test_history_url_resolves(self):
        """Test history URL resolves correctly"""
        url = reverse('ml_service:classification_history')
        self.assertEqual(url, '/api/ml/history/')
    
    def test_health_url_resolves(self):
        """Test health URL resolves correctly"""
        url = reverse('ml_service:health_check')
        self.assertEqual(url, '/api/ml/health/')


class MLServiceIntegrationTestCase(APITestCase):
    """Integration tests for ML service"""
    
    def setUp(self):
        self.classify_url = reverse('ml_service:classify_spam')
    
    @patch('apps.ml_service.views.spam_classifier.is_model_loaded')
    @patch('apps.ml_service.views.spam_classifier.predict')
    def test_end_to_end_classification(self, mock_predict, mock_is_loaded):
        """Test end-to-end classification workflow"""
        mock_is_loaded.return_value = True
        mock_predict.return_value = {
            'prediction': 'not_spam',
            'confidence': 0.75,
            'message': 'This message is not SPAM'
        }
        
        # Send classification request
        data = {'text': 'Hello, how are you today?'}
        response = self.client.post(
            self.classify_url,
            data=json.dumps(data),
            content_type='application/json'
        )
        
        # Verify response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(response_data['prediction'], 'not_spam')
        
        # Verify database record
        classification = SpamClassification.objects.get(text_input=data['text'])
        self.assertEqual(classification.prediction, 'not_spam')
        self.assertEqual(classification.confidence, 0.75)
        
        # Verify history endpoint includes this record
        history_response = self.client.get(reverse('ml_service:classification_history'))
        history_data = history_response.json()
        
        self.assertEqual(len(history_data), 1)
        self.assertEqual(history_data[0]['prediction'], 'not_spam')


class MLServicePerformanceTestCase(TestCase):
    """Performance tests for ML service"""
    
    def setUp(self):
        # Create multiple classification records
        for i in range(100):
            SpamClassification.objects.create(
                text_input=f"Test message {i}",
                prediction="spam" if i % 2 == 0 else "not_spam",
                confidence=0.8
            )
    
    def test_history_endpoint_performance(self):
        """Test that history endpoint performs well with many records"""
        with self.assertNumQueries(1):  # Should only need one query
            response = self.client.get(reverse('ml_service:classification_history'))
            self.assertEqual(response.status_code, 200)
    
    def test_history_pagination(self):
        """Test that history endpoint limits results"""
        response = self.client.get(reverse('ml_service:classification_history'))
        response_data = response.json()
        
        # Should limit to 50 results as per view implementation
        self.assertLessEqual(len(response_data), 50)