from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
import json

User = get_user_model()


class HomePageTests(TestCase):
    """Tests for the homepage"""
    
    def test_homepage_loads(self):
        """Test that homepage loads successfully"""
        response = self.client.get(reverse('main:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Welcome to Your Django Template')
    
    def test_homepage_shows_login_when_not_authenticated(self):
        """Test that homepage shows login options for anonymous users"""
        response = self.client.get(reverse('main:home'))
        self.assertContains(response, 'Login')
        self.assertContains(response, 'Sign Up')
    
    def test_homepage_shows_user_when_authenticated(self):
        """Test that homepage shows user email when authenticated"""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.force_login(user)
        response = self.client.get(reverse('main:home'))
        self.assertContains(response, 'test@example.com')
        self.assertContains(response, 'Logout')


class APIExampleTests(TestCase):
    """Tests for the example API endpoint"""
    
    def test_api_example_returns_json(self):
        """Test that API example returns JSON response"""
        response = self.client.get(reverse('main:api_example'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
    
    def test_api_example_response_structure(self):
        """Test that API example has correct response structure"""
        response = self.client.get(reverse('main:api_example'))
        data = json.loads(response.content)
        
        self.assertEqual(data['status'], 'success')
        self.assertIn('message', data)
        self.assertIn('data', data)
        self.assertIn('items', data['data'])
        self.assertEqual(data['data']['count'], 3)
    
    def test_api_example_only_accepts_get(self):
        """Test that API example only accepts GET requests"""
        response = self.client.post(reverse('main:api_example'))
        self.assertEqual(response.status_code, 405)  # Method Not Allowed


class APIProtectedTests(TestCase):
    """Tests for the protected API endpoint"""
    
    def setUp(self):
        """Create a test user"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client = Client()
    
    def test_api_protected_requires_authentication(self):
        """Test that protected API requires authentication"""
        response = self.client.get(reverse('main:api_protected'))
        # Should redirect to login
        self.assertEqual(response.status_code, 302)
    
    def test_api_protected_get_with_auth(self):
        """Test GET request to protected API with authentication"""
        self.client.force_login(self.user)
        response = self.client.get(reverse('main:api_protected'))
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        
        self.assertEqual(data['status'], 'success')
        self.assertIn('user', data)
        self.assertEqual(data['user']['email'], 'test@example.com')
    
    def test_api_protected_post_with_auth(self):
        """Test POST request to protected API with authentication"""
        self.client.force_login(self.user)
        
        test_data = {'message': 'Hello, API!', 'number': 42}
        response = self.client.post(
            reverse('main:api_protected'),
            data=json.dumps(test_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['received'], test_data)
    
    def test_api_protected_post_invalid_json(self):
        """Test POST with invalid JSON returns error"""
        self.client.force_login(self.user)
        
        response = self.client.post(
            reverse('main:api_protected'),
            data='invalid json',
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'error')


class UserModelTests(TestCase):
    """Tests for the custom User model"""
    
    def test_create_user(self):
        """Test creating a user with email"""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('testpass123'))
    
    def test_user_string_representation(self):
        """Test that user string representation is email"""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.assertEqual(str(user), 'test@example.com')
