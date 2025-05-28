from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Scholarship

class ScholarshipAPITests(APITestCase):
    def setUp(self):
        # Create sample scholarships for testing
        self.scholarship1 = Scholarship.objects.create(
            title="Scholarship A",
            description="Description A",
            amount=1000,
            provider="Provider A",
            level="Undergraduate",
            country="USA",
            field_of_study="Engineering",
            deadline="2025-12-31"
        )
        self.scholarship2 = Scholarship.objects.create(
            title="Scholarship B",
            description="Description B",
            amount=2000,
            provider="Provider B",
            level="Postgraduate",
            country="Canada",
            field_of_study="Medicine",
            deadline="2025-11-30"
        )

    def test_list_scholarships(self):
        # Test the list endpoint
        response = self.client.get('/api/scholarships/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_scholarship(self):
        # Test the retrieve endpoint
        response = self.client.get(f'/api/scholarships/{self.scholarship1.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Scholarship A")

    def test_search_scholarships(self):
        # Test the search functionality
        response = self.client.get('/api/scholarships/?search=Engineering')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "Scholarship A")

    def test_filter_scholarships(self):
        # Test the filter functionality
        response = self.client.get('/api/scholarships/?country=Canada')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "Scholarship B")
