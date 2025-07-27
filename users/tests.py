from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile
from users.models import User
import io
import csv

class CSVUploadTests(APITestCase):
    def setUp(self):
        self.url = reverse('upload-csv')

    def create_csv_file(self, rows):
        csv_data = io.StringIO()
        writer = csv.writer(csv_data)
        writer.writerow(['name', 'email', 'age'])  # headers
        writer.writerows(rows)
        csv_data.seek(0)
        return SimpleUploadedFile("test.csv", csv_data.read().encode(), content_type="text/csv")

    def test_valid_and_invalid_records(self):
        rows = [
            ['Alice', 'alice@example.com', '30'],       # valid
            ['Bob', 'invalid-email', '25'],             # invalid email
            ['', 'charlie@example.com', '40'],          # empty name
            ['Dan', 'dan@example.com', '130'],          # invalid age
        ]
        file = self.create_csv_file(rows)
        response = self.client.post(self.url, {'file': file}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['saved_records'], 1)
        self.assertEqual(response.data['rejected_records'], 3)
        self.assertEqual(User.objects.count(), 1)

    def test_duplicate_email_skipped(self):
        User.objects.create(name='Eve', email='eve@example.com', age=28)
        rows = [['Eve Duplicate', 'eve@example.com', '35']]
        file = self.create_csv_file(rows)
        response = self.client.post(self.url, {'file': file}, format='multipart')
        self.assertEqual(response.data['saved_records'], 0)
        self.assertEqual(response.data['rejected_records'], 1)
        self.assertIn('user with this email already exists', str(response.data['validation_errors']))

    def test_non_csv_file_rejected(self):
        bad_file = SimpleUploadedFile("test.txt", b"bad content", content_type="text/plain")
        response = self.client.post(self.url, {'file': bad_file}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Only CSV files are allowed", response.data['error'])
