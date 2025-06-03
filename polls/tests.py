from django.test import TestCase
from polls.models import CustomUser

class CustomUserModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email="testuser@example.com",
            password="securepassword123",
            first_name="Test",
            last_name="User",
            phone_number="1234567890"
        )

    def test_user_creation(self):
        self.assertEqual(self.user.email, "testuser@example.com")
        self.assertTrue(self.user.check_password("securepassword123"))
        self.assertEqual(self.user.first_name, "Test")
        self.assertEqual(self.user.last_name, "User")
        self.assertEqual(self.user.phone_number, "1234567890")

    def test_string_representation(self):
        self.assertEqual(str(self.user), "Test User")

    def test_user_default_values(self):
        self.assertFalse(self.user.is_superuser)
        self.assertFalse(self.user.is_staff)
