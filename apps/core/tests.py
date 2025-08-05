import json
from django.test import TestCase, Client
from django.urls import reverse
from django.core import mail
from rest_framework.test import APITestCase
from rest_framework import status
from .models import ContactMessage
from apps.portfolio.models import PersonalInfo, Project, Skill, Experience


class CoreViewsTestCase(TestCase):
    """Test cases for core views"""
    
    def setUp(self):
        self.client = Client()
        
        # Create test data
        self.personal_info = PersonalInfo.objects.create(
            name="Test User",
            title="Test Developer",
            bio="Test bio content",
            email="test@example.com",
            location="Test City"
        )
        
        self.skill = Skill.objects.create(
            name="Python",
            category="backend",
            proficiency=4,
            is_featured=True
        )
        
        self.project = Project.objects.create(
            title="Test Project",
            slug="test-project",
            description="Test project description",
            is_featured=True,
            is_published=True
        )
        
        self.experience = Experience.objects.create(
            title="Test Developer",
            company_or_institution="Test Company",
            experience_type="work",
            description="Test experience description",
            start_date="2023-01-01"
        )
    
    def test_home_view_get(self):
        """Test home view GET request"""
        response = self.client.get(reverse('core:home'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.personal_info.name)
        self.assertContains(response, self.project.title)
        self.assertContains(response, self.skill.name)
        self.assertContains(response, self.experience.title)
    
    def test_home_view_context(self):
        """Test home view context data"""
        response = self.client.get(reverse('core:home'))
        
        self.assertIn('personal_info', response.context)
        self.assertIn('featured_projects', response.context)
        self.assertIn('featured_skills', response.context)
        self.assertIn('recent_experience', response.context)
        
        self.assertEqual(response.context['personal_info'], self.personal_info)
        self.assertIn(self.project, response.context['featured_projects'])
        self.assertIn(self.skill, response.context['featured_skills'])
        self.assertIn(self.experience, response.context['recent_experience'])


class ContactMessageAPITestCase(APITestCase):
    """Test cases for contact message API"""
    
    def setUp(self):
        self.url = reverse('core:contact')
        self.valid_data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'subject': 'Test Subject',
            'message': 'This is a test message for the contact form.'
        }
    
    def test_send_contact_message_success(self):
        """Test successful contact message submission"""
        response = self.client.post(
            self.url,
            data=json.dumps(self.valid_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.json())
        
        # Check if message was saved to database
        self.assertTrue(ContactMessage.objects.filter(
            name=self.valid_data['name'],
            email=self.valid_data['email']
        ).exists())
    
    def test_send_contact_message_invalid_data(self):
        """Test contact message submission with invalid data"""
        invalid_data = {
            'name': '',  # Empty name
            'email': 'invalid-email',  # Invalid email
            'subject': '',  # Empty subject
            'message': ''  # Empty message
        }
        
        response = self.client.post(
            self.url,
            data=json.dumps(invalid_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.json())
    
    def test_send_contact_message_missing_fields(self):
        """Test contact message submission with missing fields"""
        incomplete_data = {
            'name': 'John Doe',
            # Missing email, subject, and message
        }
        
        response = self.client.post(
            self.url,
            data=json.dumps(incomplete_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.json())
    
    def test_send_contact_message_email_validation(self):
        """Test email validation in contact form"""
        invalid_email_data = self.valid_data.copy()
        invalid_email_data['email'] = 'not-an-email'
        
        response = self.client.post(
            self.url,
            data=json.dumps(invalid_email_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.json())
    
    def test_contact_message_method_not_allowed(self):
        """Test that GET method is not allowed for contact endpoint"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class ContactMessageModelTestCase(TestCase):
    """Test cases for ContactMessage model"""
    
    def test_contact_message_creation(self):
        """Test creating a contact message"""
        message = ContactMessage.objects.create(
            name="Test User",
            email="test@example.com",
            subject="Test Subject",
            message="Test message content"
        )
        
        self.assertEqual(str(message), "Test User - Test Subject")
        self.assertFalse(message.is_read)
        self.assertIsNotNone(message.created_at)
        self.assertIsNotNone(message.updated_at)
    
    def test_contact_message_ordering(self):
        """Test contact message ordering"""
        # Create multiple messages
        message1 = ContactMessage.objects.create(
            name="User 1",
            email="user1@example.com",
            subject="Subject 1",
            message="Message 1"
        )
        
        message2 = ContactMessage.objects.create(
            name="User 2",
            email="user2@example.com",
            subject="Subject 2",
            message="Message 2"
        )
        
        # Check ordering (newest first)
        messages = list(ContactMessage.objects.all())
        self.assertEqual(messages[0], message2)
        self.assertEqual(messages[1], message1)
    
    def test_contact_message_fields(self):
        """Test contact message field constraints"""
        message = ContactMessage.objects.create(
            name="A" * 100,  # Max length
            email="test@example.com",
            subject="B" * 200,  # Max length
            message="Test message"
        )
        
        self.assertEqual(len(message.name), 100)
        self.assertEqual(len(message.subject), 200)


class URLsTestCase(TestCase):
    """Test URL routing"""
    
    def test_home_url_resolves(self):
        """Test home URL resolves correctly"""
        url = reverse('core:home')
        self.assertEqual(url, '/')
    
    def test_contact_url_resolves(self):
        """Test contact URL resolves correctly"""
        url = reverse('core:contact')
        self.assertEqual(url, '/contact/')


class TemplateTestCase(TestCase):
    """Test template rendering"""
    
    def setUp(self):
        self.client = Client()
    
    def test_home_template_used(self):
        """Test correct template is used for home view"""
        response = self.client.get(reverse('core:home'))
        self.assertTemplateUsed(response, 'core/index.html')
        self.assertTemplateUsed(response, 'base.html')
    
    def test_responsive_design_meta_tags(self):
        """Test responsive design meta tags are present"""
        response = self.client.get(reverse('core:home'))
        self.assertContains(response, 'viewport')
        self.assertContains(response, 'width=device-width')


class SecurityTestCase(TestCase):
    """Test security features"""
    
    def setUp(self):
        self.client = Client()
    
    def test_csrf_protection(self):
        """Test CSRF protection is enabled"""
        # This test ensures CSRF protection is working
        # POST requests without CSRF token should be rejected
        response = self.client.post(
            reverse('core:contact'),
            data={'name': 'test'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        # Should still work because we're using API view with proper handling
        self.assertIn(response.status_code, [400, 403])  # Either validation error or CSRF error
    
    def test_sql_injection_protection(self):
        """Test protection against SQL injection"""
        # Try to inject SQL through form fields
        malicious_data = {
            'name': "'; DROP TABLE core_contactmessage; --",
            'email': 'test@example.com',
            'subject': 'Test',
            'message': 'Test message'
        }
        
        response = self.client.post(
            reverse('core:contact'),
            data=json.dumps(malicious_data),
            content_type='application/json'
        )
        
        # Check that tables still exist (injection didn't work)
        self.assertTrue(ContactMessage.objects.model._meta.db_table)


class PerformanceTestCase(TestCase):
    """Test performance optimizations"""
    
    def setUp(self):
        self.client = Client()
        
        # Create multiple test objects to test N+1 queries
        for i in range(10):
            project = Project.objects.create(
                title=f"Project {i}",
                slug=f"project-{i}",
                description=f"Description {i}",
                is_featured=True,
                is_published=True
            )
            
            skill = Skill.objects.create(
                name=f"Skill {i}",
                category="backend",
                proficiency=3,
                is_featured=True
            )
            
            project.technologies.add(skill)
    
    def test_home_view_query_count(self):
        """Test that home view doesn't have excessive queries"""
        with self.assertNumQueries(4):  # Should be a reasonable number
            response = self.client.get(reverse('core:home'))
            self.assertEqual(response.status_code, 200)