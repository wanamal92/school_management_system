from django.test import TestCase
from students.models import Student

class StudentModelTest(TestCase):
    def test_full_name(self):
        student = Student.objects.create(
            first_name='John',
            last_name='Doe',
            student_number='S12345',
            date_of_birth='2005-06-15'
        )
        self.assertEqual(str(student), 'John Doe')  # Ensure full name is correct

from django.test import TestCase
from students.models import Student
from django.contrib.auth import get_user_model

class StudentSignalTest(TestCase):
    def test_student_creation_creates_user(self):
        student = Student.objects.create(
            first_name='Jane',
            last_name='Doe',
            student_number='S12346',
            date_of_birth='2006-06-15'
        )
        user = get_user_model().objects.get(username='janed')
        self.assertIsNotNone(user)
        self.assertEqual(user.role, 'student')
