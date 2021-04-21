from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class WeatherRestApiTest(APITestCase):
    def setUp(self) -> None:
        self.index_endpoint = reverse('weather_rest:index')

    def test_index_endpoint_get_method(self):
        """here we test that index endpoint is working"""
        response = self.client.get(self.index_endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_index_endpoint_post_method(self):
        """testing indexview with a city name"""
        response = self.client.post(self.index_endpoint, data={'city': 'marivan'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('name', response.data)
        self.assertIn('lat', response.data)
        self.assertIn('lon', response.data)

    def test_index_endpoint_post_wrong_data(self):
        """testing sending wrong city name"""
        response = self.client.post(self.index_endpoint, {'city': 'asdf'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_index_endpoint_with_city(self):
        """adding a city to session and after return it's data"""
        response = self.client.post(self.index_endpoint, {'city': 'marivan'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(self.index_endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Marivan', response.data[0]['name'])

    def test_new_session(self):
        """test flushing session"""
        url = reverse('weather_rest:new-session')
        self.client.post(self.index_endpoint, {'city': 'marivan'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(self.index_endpoint)
        self.assertEqual(len(response.data), 1)

    def test_removing_city(self):
        """testing removing city from session"""
        self.client.post(self.index_endpoint, {'city': 'Marivan'})
        url = reverse('weather_rest:remove-city')
        response = self.client.get(url, {'city': 'Marivan'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(self.index_endpoint)
        self.assertEqual(len(response.data), 1)
