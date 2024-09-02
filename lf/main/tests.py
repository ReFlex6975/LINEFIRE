from django.test import TestCase
from .models import Equipment

class EquipmentModelTest(TestCase):
    def test_string_representation(self):
        equipment = Equipment(name="Test Equipment")
        self.assertEqual(str(equipment), equipment.name)
