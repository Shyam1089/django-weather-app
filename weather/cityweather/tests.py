import unittest
from unittest import mock
from unittest.mock import patch, Mock
from django.test import TestCase
from django.urls import reverse
from cityweather.forms import InputForm
from cityweather import views
import requests

class ViewsTest(unittest.TestCase):

    def mock_response(
            self,
            status=200,
            content="CONTENT",
            json_data=None,
            method='GET',
            raise_for_status=None):
        """
        since we typically test a bunch of different
        requests calls for a service, we are going to do
        a lot of mock responses, so its usually a good idea
        to have a helper function that builds these things
        """
        mock_resp = mock.Mock()
        # mock raise_for_status call w/optional error
        mock_resp.raise_for_status = mock.Mock()
        if raise_for_status:
            mock_resp.raise_for_status.side_effect = raise_for_status
        # set status code and content
        mock_resp.status_code = status
        mock_resp.content = content
        mock_resp.method = method
        # add json data if provided
        if json_data:
            mock_resp.json = mock.Mock(
                return_value=json_data
            )
        return mock_resp


    def test_get_wind_direction_success(self):
        response = views.get_wind_direction(123)
        expected_result = "South East"
        self.assertEqual(response, expected_result)


    def test_get_wind_direction_success2(self):
        response = views.get_wind_direction(0)
        expected_result = "North"
        self.assertEqual(response, expected_result)


    def test_get_weather_data_negative(self):
        response = views.get_weather_data("DUMMY CITY", 'en')
        expected_result = {'cod': '404', 'msg': 'city not found'}
        self.assertEqual(response.keys(), expected_result.keys())

    @patch("cityweather.views.get_weather_data")
    @patch("cityweather.views.requests.post")
    @patch("cityweather.views.get_weather_data")
    def test_homepage(self, mock_get_weather_data, mock_request_post, mock_api_call):
        mock_api_call.all.return_value = {'cod': '404', 'msg': 'city not found'}
        mock_request_post.return_value =  self.mock_response(status=200, content='{"result": "true"}', method='POST')
        result = views.homepage(mock_request_post)
        self.assertEqual(result.status_code, 200)

    def test_generate_cache_key(self):
        response = views.generate_cache_key("new York", "en")
        expected_result = "new york", "en-new-york"
        self.assertEqual(response, expected_result)

    def test_generate_cache_key_extra_spaces(self):
        response = views.generate_cache_key("   New York   ", "en")
        expected_result = "new york", "en-new-york"
        self.assertEqual(response, expected_result)