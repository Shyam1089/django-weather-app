import requests
import json

from django.shortcuts import render
from django.http import HttpResponse
from django import forms
from django.utils.translation import gettext as _
from django.core.cache import cache


class InputForm(forms.Form):
    search = forms.CharField(label=_("Select City"),
                             max_length=50, localize=True)


def homepage(request):
    weather_data = {}
    if request.method == 'POST':
        form = InputForm(request.POST)
        if form.is_valid():
            pass  # does nothing, just trigger the validation
        city = form.cleaned_data.get('search', "").lower()
        if city:
            cached_data = cache.get(city, False)
            if not cached_data:
                print("calling API")
                weather_data = get_weather_data(city, request.LANGUAGE_CODE)
                if weather_data.get('cod', "") != '404':
                    weather_data.update(
                        {"wind_direction": get_wind_direction(weather_data['wind']['deg'])})
                    cache.add(city, weather_data)
            else:
                weather_data = cache.get(city)
    else:
        form = InputForm()
    return render(request, 'cityweather/homepage.html', {'form': form, 'data': weather_data})


def get_weather_data(city_name, lang):
    API_KEY = "8a7f5047848c86496d086cc4f1f243ba"
    response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}&lang={lang}&units=metric")
    return json.loads(response.content)


def get_wind_direction(degree):
    if (degree > 337.5):
        return 'North'
    if (degree > 292.5):
        return 'North West'
    if(degree > 247.5):
        return 'West'
    if(degree > 202.5):
        return 'South West'
    if(degree > 157.5):
        return 'South'
    if(degree > 122.5):
        return 'South East'
    if(degree > 67.5):
        return 'East'
    if(degree > 22.5):
        return 'North East'
    return 'North'
