import requests
import json

from django.shortcuts import render
from django.http import HttpResponse
from .forms import InputForm
from django.core.cache import cache
from django.utils.translation import gettext as _


def homepage(request):
    weather_data = {}
    if request.method == 'POST':
        form = InputForm(request.POST)
        if form.is_valid():
            pass  # does nothing, just trigger the validation
        city = form.cleaned_data.get('search', "").lower()
        if city:
            try:
                cached_data = cache.get(city, False)
                if not cached_data:
                    weather_data = get_weather_data(city, request.LANGUAGE_CODE)
                    if str(weather_data.get('cod', "")) == '200':
                        weather_data.update({
                            "wind_direction": get_wind_direction(weather_data['wind']['deg'])
                        })
                        cache.add(city, weather_data)
                else:
                    weather_data = cache.get(city)
            except:
                weather_data.update({"cod":500, "msg":_("Internal Server Error! Please try later.")})
    else:
        form = InputForm()
    print (weather_data)
    return render(request, 'cityweather/homepage.html', {'form': form, 'data': weather_data})


def get_weather_data(city_name, lang):
    API_KEY = "8a7f5047848c86496d086cc4f1f243ba"
    try:
        response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}&lang={lang}&units=metric")
        if response.status_code == 200:
            return json.loads(response.content)
        elif response.status_code == 404:
            return {"cod":404, "msg":_("City not found! Please enter another city.")}
    except Exception as e:
        print (e)
    return {"cod":500, "msg":_("Network Error! Please try later.")}


def get_wind_direction(degree):
    print (degree)
    if (degree > 337.5):
        return _('North')
    if (degree > 292.5):
        return _('North West')
    if(degree > 247.5):
        return _('West')
    if(degree > 202.5):
        return _('South West')
    if(degree > 157.5):
        return _('South')
    if(degree > 122.5):
        return _('South East')
    if(degree > 67.5):
        return _('East')
    if(degree > 22.5):
        return _('North East')
    return _('North')
