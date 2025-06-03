from django.test import TestCase
from properties.models import Property
from polls.models import CustomUser

class PropertyModelTest(TestCase):
    def setUp(self):
        self.owner = CustomUser.objects.create_user(
            email="owner@example.com",
            password="securepassword123",
            first_name="Owner",
            last_name="Test",
            phone_number="9876543210"
        )
        self.property = Property.objects.create(
            title="Beautiful House",
            description="A lovely 3-bedroom house.",
            price=250000,
            location="123 Main Street, Springfield",
            size=120,
            owner=self.owner,
        )

    def test_property_creation(self):
        self.assertEqual(self.property.title, "Beautiful House")
        self.assertEqual(self.property.description, "A lovely 3-bedroom house.")
        self.assertEqual(self.property.price, 250000)
        self.assertEqual(self.property.location, "123 Main Street, Springfield")
        self.assertEqual(self.property.size, 120)
        self.assertEqual(self.property.owner, self.owner)

    def test_string_representation(self):
        self.assertEqual(str(self.property), "Beautiful House")

    def test_property_default_values(self):
        self.assertIsNotNone(self.property.publication_date)
