import random
import requests
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from . import api_keys
from .serializers import CitySerializer

OPEN_WEATHER_API_KEY = getattr(api_keys, 'OPEN_WEATHER_API_KEY')
PEXEL_API_KEY  = getattr(api_keys, 'PEXEL_API_KEY')


class IndexView(APIView):
    def get(self, request, *args, **kwargs):
        """get method"""
        session = request.session
        cities = [session[key] for key in session.keys() if key.startswith('city_')]
        data = []
        for city in cities:
            data.append(self.get_city_weather(city))
        data.append({'image-url': self.get_image_url()})
        return Response(data)

    def get_image_url(self):
        url = "https://api.pexels.com/v1/search?query=landscape&orientation=landscape" \
              f"&Authorization={PEXEL_API_KEY}&size=large&per_page=80"
        response = requests.get(url,
                                headers={
                                    'authorization': PEXEL_API_KEY
                                }).json()
        if 'error' in response:
            return ''
        image_data = random.choice(response['photos'])
        return image_data['src']['original']

    def get_city_weather(self, city):
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={OPEN_WEATHER_API_KEY }'
        response = requests.get(url).json()
        if response['cod'] != status.HTTP_200_OK:
            return {'error': 'Wrong city name'}
        return {
            **response['coord'],
            'name': response['name'],
            'wind': response['wind'],
            'temp': response['main']['temp'],
            'description': response['weather'][0]['description'],
            'icon': response['weather'][0]['icon']
        }

    def post(self, request, *args, **kwargs):
        """testing post method for adding city"""
        serializer = CitySerializer(request.data)
        city_data = self.get_city_weather(serializer.data.get('city'))
        if 'error' in city_data:
            return Response(city_data, status=status.HTTP_400_BAD_REQUEST)
        session = request.session
        city_name = f'city_{city_data["name"]}'
        session[city_name] = city_data['name']
        return Response(city_data)


class NewSessionView(APIView):
    def get(self, request, *args, **kwargs):
        request.session.flush()
        return Response()


class RemoveCity(APIView):
    def get(self, request, *args, **kwargs):
        serializer = CitySerializer(request.GET)
        city_name = serializer.data.get('city')
        if f'city_{city_name}' in request.session.keys():
            del request.session[f'city_{city_name}']
        return Response({'msg': 'city has been removed'})
