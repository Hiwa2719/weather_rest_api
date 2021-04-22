from unittest import mock

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from . import api_keys

OPEN_WEATHER_API_KEY = getattr(api_keys, 'OPEN_WEATHER_API_KEY')
PEXEL_API_KEY = getattr(api_keys, 'PEXEL_API_KEY')


city_response = {
    "coord": {
        "lon": -122.08,
        "lat": 37.39
    },
    "weather": [
        {
            "id": 800,
            "main": "Clear",
            "description": "clear sky",
            "icon": "01d"
        }
    ],
    "base": "stations",
    "main": {
        "temp": 282.55,
        "feels_like": 281.86,
        "temp_min": 280.37,
        "temp_max": 284.26,
        "pressure": 1023,
        "humidity": 100
    },
    "visibility": 16093,
    "wind": {
        "speed": 1.5,
        "deg": 350
    },
    "clouds": {
        "all": 1
    },
    "dt": 1560350645,
    "sys": {
        "type": 1,
        "id": 5122,
        "message": 0.0139,
        "country": "US",
        "sunrise": 1560343627,
        "sunset": 1560396563
    },
    "timezone": -25200,
    "id": 420006353,
    "name": "Marivan",
    "cod": 200
}
wrong_city_name = {'cod': 400}
lat_lon_response = {
    "lat": 33.44,
    "lon": -94.04,
    "timezone": "America/Chicago",
    "timezone_offset": -21600,
    "current": {
        "dt": 1618317040,
        "sunrise": 1618282134,
        "sunset": 1618333901,
        "temp": 284.07,
        "feels_like": 282.84,
        "pressure": 1019,
        "humidity": 62,
        "dew_point": 277.08,
        "uvi": 0.89,
        "clouds": 0,
        "visibility": 10000,
        "wind_speed": 6,
        "wind_deg": 300,
        "weather": [
            {
                "id": 500,
                "main": "Rain",
                "description": "light rain",
                "icon": "10d"
            }
        ],
        "rain": {
            "1h": 0.21
        }
    },
    "minutely": [
        {
            "dt": 1618317060,
            "precipitation": 0.205
        }],
    "hourly": [
        {
            "dt": 1618315200,
            "temp": 282.58,
            "feels_like": 280.4,
            "pressure": 1019,
            "humidity": 68,
            "dew_point": 276.98,
            "uvi": 1.4,
            "clouds": 19,
            "visibility": 306,
            "wind_speed": 4.12,
            "wind_deg": 296,
            "wind_gust": 7.33,
            "weather": [
                {
                    "id": 801,
                    "main": "Clouds",
                    "description": "few clouds",
                    "icon": "02d"
                }
            ],
            "pop": 0
        }
    ],
    "daily": [
        {
            "dt": 1618308000,
            "sunrise": 1618282134,
            "sunset": 1618333901,
            "moonrise": 1618284960,
            "moonset": 1618339740,
            "moon_phase": 0.04,
            "temp": {
                "day": 279.79,
                "min": 275.09,
                "max": 284.07,
                "night": 275.09,
                "eve": 279.21,
                "morn": 278.49
            },
            "feels_like": {
                "day": 277.59,
                "night": 276.27,
                "eve": 276.49,
                "morn": 276.27
            },
            "pressure": 1020,
            "humidity": 81,
            "dew_point": 276.77,
            "wind_speed": 3.06,
            "wind_deg": 294,
            "weather": [
                {
                    "id": 500,
                    "main": "Rain",
                    "description": "light rain",
                    "icon": "10d"
                }
            ],
            "clouds": 56,
            "pop": 0.2,
            "rain": 0.62,
            "uvi": 1.93
        }]
}
days_hours_response = {
  "cod": "200",
  "message": 0,
  "cnt": 40,
  "list": [
    {
      "dt": 1596564000,
      "main": {
        "temp": 293.55,
        "feels_like": 293.13,
        "temp_min": 293.55,
        "temp_max": 294.05,
        "pressure": 1013,
        "sea_level": 1013,
        "grnd_level": 976,
        "humidity": 84,
        "temp_kf": -0.5
      },
      "weather": [
        {
          "id": 500,
          "main": "Rain",
          "description": "light rain",
          "icon": "10d"
        }
      ],
      "clouds": {
        "all": 38
      },
      "wind": {
        "speed": 4.35,
        "deg": 309,
        "gust": 7.87
      },
      "visibility": 10000,
      "pop": 0.49,
      "rain": {
        "3h": 0.53
      },
      "sys": {
        "pod": "d"
      },
      "dt_txt": "2020-08-04 18:00:00"
    },
],
"city": {
    "id": 2643743,
    "name": "London",
    "coord": {
      "lat": 51.5073,
      "lon": -0.1277
    },
    "country": "GB",
    "timezone": 0,
    "sunrise": 1578384285,
    "sunset": 1578413272
  }
}


def requests_patch_side_effect(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data
    if args[0] == f'http://api.openweathermap.org/data/2.5/weather?q=Marivan&units=metric&appid={OPEN_WEATHER_API_KEY}':
        return MockResponse(city_response, 200)
    if args[0] == f'http://api.openweathermap.org/data/2.5/weather?q=asdf&units=metric&appid={OPEN_WEATHER_API_KEY}':
        return MockResponse(wrong_city_name, 400)
    url = "https://api.pexels.com/v1/search?query=landscape&orientation=landscape" \
          f"&Authorization={PEXEL_API_KEY}&size=large&per_page=80"
    if args[0] == url:
        return MockResponse({
            'photos': [{
                'src':
                    {
                        'original': 'original'
                    }
            }]
        }, 200)

    url = "https://api.openweathermap.org/data/2.5/onecall?lat=35.5219&lon=46.176" \
          f"&units=metric&exclude=current,minutely,hourly,alerts&appid={OPEN_WEATHER_API_KEY}"
    if args[0] == url:
        return MockResponse(lat_lon_response, 200)
    url =f'http://api.openweathermap.org/data/2.5/forecast?q=Marivan&units=metric&appid={OPEN_WEATHER_API_KEY}'
    if args[0] == url:
        return MockResponse(days_hours_response, 200)


@mock.patch('weather_rest.views.requests.get', side_effect=requests_patch_side_effect)
class WeatherRestApiTest(APITestCase):
    def setUp(self) -> None:
        self.index_endpoint = reverse('weather_rest:index')

    def test_index_endpoint_get_method(self, mock_obj):
        """here we test that index endpoint is working"""
        response = self.client.get(self.index_endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_index_endpoint_post_method(self, mock_obj):
        """testing indexview with a city name"""
        response = self.client.post(self.index_endpoint, data={'city': 'Marivan'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('name', response.data)
        self.assertIn('lat', response.data)
        self.assertIn('lon', response.data)

    def test_index_endpoint_post_wrong_data(self, mock_obj):
        """testing sending wrong city name"""
        response = self.client.post(self.index_endpoint, {'city': 'asdf'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_index_endpoint_with_city(self, mock_obj):
        """adding a city to session and after return it's data"""
        response = self.client.post(self.index_endpoint, {'city': 'Marivan'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(self.index_endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Marivan', response.data[0]['name'])

    def test_new_session(self, mock_obj):
        """test flushing session"""
        url = reverse('weather_rest:new-session')
        self.client.post(self.index_endpoint, {'city': 'Marivan'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(self.index_endpoint)
        self.assertEqual(len(response.data), 1)

    def test_removing_city(self, mock_obj):
        """testing removing city from session"""
        self.client.post(self.index_endpoint, {'city': 'Marivan'})
        url = reverse('weather_rest:remove-city')
        response = self.client.get(url, {'city': 'Marivan'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(self.index_endpoint)
        self.assertEqual(len(response.data), 1)

    # @mock.patch('weather_rest.views.requests', return_value=True)
    def test_getting_weather_data_on_lat_lon(self, mock_obj):
        """getting weather data based on latitude and longitude"""
        url = reverse('weather_rest:weather-detail')
        response = self.client.get(url, {'lon': 46.176, 'lat': 35.5219, 'city': 'Marivan'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('days', response.data)
