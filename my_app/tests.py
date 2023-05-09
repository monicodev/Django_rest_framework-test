from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import ChargePoint


# Create your tests here.


class ChargePointModelTest(TestCase):

    def test_create_charge_point(self):
        initial_count = ChargePoint.objects.count()
        new_charge_point = ChargePoint.objects.create(name='Test Charge Point')
        new_count = ChargePoint.objects.count()
        self.assertEqual(initial_count + 1, new_count)
        self.assertEqual(new_charge_point.name, 'Test Charge Point')
        self.assertEqual(new_charge_point.status, ChargePoint.STATUS_READY)
        self.assertIsInstance(new_charge_point, ChargePoint)

    def test_create_duplicate_charge_point(self):
        ChargePoint.objects.create(name='Test Charge Point')
        with self.assertRaises(IntegrityError):
            ChargePoint.objects.create(name='Test Charge Point')

    def test_update_charge_point(self):
        charge_point = ChargePoint.objects.create(name='Test Charge Point')
        charge_point.name = 'Updated Charge Point'
        charge_point.status = ChargePoint.STATUS_CHARGING
        charge_point.save()
        updated_charge_point = ChargePoint.objects.get(id=charge_point.id)
        self.assertEqual(updated_charge_point.name, 'Updated Charge Point')
        self.assertEqual(updated_charge_point.status, ChargePoint.STATUS_CHARGING)

    def test_delete_charge_point(self):
        charge_point = ChargePoint.objects.create(name='Test Charge Point')
        initial_count = ChargePoint.objects.count()
        charge_point.delete()
        new_count = ChargePoint.objects.count()
        self.assertEqual(initial_count - 1, new_count)

    def test_get_deleted_charge_point(self):
        charge_point = ChargePoint.objects.create(name='Test Charge Point')
        charge_point.delete()
        with self.assertRaises(ChargePoint.DoesNotExist):
            ChargePoint.objects.get(id=charge_point.id)

    def test_get_charge_points(self):
        ChargePoint.objects.create(name='Test Charge Point 1')
        ChargePoint.objects.create(name='Test Charge Point 2')
        response = self.client.get(reverse('charge_point:list_or_create_charge_point'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_create_charge_point_with_invalid_status(self):
        invalid_status = 5
        charge_point = ChargePoint(name='Test Charge Point', status=invalid_status)
        with self.assertRaises(ValidationError) as context:
            charge_point.full_clean()
        self.assertIn('status', context.exception.message_dict)


class ChargePointAPITests(APITestCase):

    def setUp(self):
        self.charge_point_data = {
            'name': 'Charge Point 1',
            'status': ChargePoint.STATUS_READY
        }

    url_list_or_create = reverse('charge_point:list_or_create_charge_point')
    invalid_url_RUD = reverse('charge_point:get_update_or_delete_charge_point', args=[9999])  # ID inexistente

    def test_list_charge_points(self):
        response = self.client.get(self.url_list_or_create)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_charge_point(self):
        response = self.client.post(self.url_list_or_create, data=self.charge_point_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def get_valid_url_RUD(self):
        charge_point = ChargePoint.objects.create(name='Charge Point 1', status=ChargePoint.STATUS_READY)
        return reverse('charge_point:get_update_or_delete_charge_point', args=[charge_point.id])

    def test_get_charge_point(self):
        response = self.client.get(self.get_valid_url_RUD())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_charge_point(self):
        updated_data = {'name': 'Updated Charge Point', 'status': ChargePoint.STATUS_CHARGING}
        response = self.client.put(self.get_valid_url_RUD(), data=updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_charge_point(self):
        response = self.client.delete(self.get_valid_url_RUD())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_charge_point(self):
        response = self.client.get(self.invalid_url_RUD)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_invalid_charge_point(self):
        updated_data = {'name': 'Updated Charge Point', 'status': ChargePoint.STATUS_ERROR}
        response = self.client.put(self.invalid_url_RUD, data=updated_data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_invalid_charge_point(self):
        response = self.client.delete(self.invalid_url_RUD)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_invalid_charge_point(self):
        invalid_data = {
            'status': ChargePoint.STATUS_ERROR,  # 'name' field is missing
        }
        response = self.client.post(self.url_list_or_create, data=invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_charge_point_with_invalid_data(self):
        invalid_data = {'name': ''}  # 'name' field can't be blank
        response = self.client.post(self.url_list_or_create, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_charge_point_with_duplicate_name(self):
        ChargePoint.objects.create(name='Test Charge Point')
        duplicate_data = {'name': 'Test Charge Point'}
        response = self.client.post(self.url_list_or_create, duplicate_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_charge_point_with_invalid_status(self):
        invalid_data = {'name': 'Test Charge Point', 'status': 5}
        response = self.client.post(self.url_list_or_create, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
