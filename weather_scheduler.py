#!/usr/bin/env python3

"""
weather_scheduler is Python code to gather weather data and schedule events.

Copyright 2016 Matthew Bruzek

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import argparse
import datetime
import requests
import sys
import traceback

from datetime import date
from datetime import time
from datetime import timedelta
from jinja2 import Template


CONTEXT = 'Additional comma separated key=value pairs to use as context'
DAY = 'The day of the week to use weather data for: \n' \
      'monday|tuesday|wednesday|thursday|friday|saturday|sunday'
DEFAULT_LOCATION = 'MN/Rochester'
DEFAULT_URL = 'http://i118.photobucket.com/albums/o117/dave6167/Bicycle%20Sports%20Maps/BS{{ wind_direction }}.gif'  # noqa
DESCRIPTION = 'Request weather forecast data from the Internet and render ' \
              'an event template.'
DEBUG = False
KEY = 'The weather underground key to use when making the API requests'
LOCATION = 'The location to query for the weather forecast'
NOW = datetime.datetime.now()  # The current date with time.
TIME = 'The time of the event in "HH:MM AM|PM" format'
URL = 'The url to the image to use for the image of the event. Hint you can ' \
      'use context variables in the url'
WEEK = {'monday': 0,
        'tuesday': 1,
        'wednesday': 2,
        'thursday': 3,
        'friday': 4,
        'saturday': 5,
        'sunday': 6}


def command_line():
    """The function to parse the arguments from the command line."""
    try:
        parser = argparse.ArgumentParser(description=DESCRIPTION)
        parser.add_argument('-c', '--context',
                            help='{0} [{1}]'.format(CONTEXT, None))
        parser.add_argument('-d', '--day', default='monday',
                            help='{0} [{1}]'.format(DAY, 'monday'))
        parser.add_argument('-k', '--key',
                            help='{0} [{1}]'.format(KEY, None))
        parser.add_argument('-l', '--location', default=DEFAULT_LOCATION,
                            help='{0} [{1}]'.format(LOCATION, None))
        parser.add_argument('-t', '--time', default='6:00 PM',
                            help='{0} [{1}]'.format(TIME, '6:00 PM'))
        arguments = parser.parse_args()
        # Parse the time HH:MM AM|PM from the command line.
        start = datetime.datetime.strptime(arguments.time, '%I:%M %p').time()
        print(schedule_event(split_kv_string(arguments.context),
                             arguments.day,
                             arguments.key,
                             arguments.location,
                             start))
    except:
        print('An exception occurred parsing the command-line arguments.')
        print(traceback.print_exc())
        exit(1)


def interactive():
    """Interactively prompt the user for required values."""
    options = {}
    try:
        options['context'] = prompt(CONTEXT)
        options['day'] = prompt(DAY, 'monday')
        options['key'] = prompt(KEY)
        options['location'] = prompt(LOCATION, DEFAULT_LOCATION)
        time = prompt(TIME, '6:00 PM')
        # Parse the time HH:MM AM|PM from user input.
        options['time'] = datetime.datetime.strptime(time, '%I:%M %p').time()
        print(schedule_event(split_kv_string(options['context']),
                             options['day'],
                             options['key'],
                             options['location'],
                             options['time']))
    except (KeyboardInterrupt, SystemExit) as e:
        print('\n\nUser has quit, exiting program.')
        exit(2)


def split_kv_string(string):
    """Split the string on commas and then split the remaining elements on
    equal sign to create a dict of key and value pairs."""
    dictionary = {}
    # Are there any commas in the string?
    if ',' in string:
        array = string.split(',')  # Split on commas first.
    else:
        array = [string]  # No commas so put string in array to parse it.
    # Now parse the array for key & value pairs.
    for kv in array:
        key, value = kv.split('=')
        dictionary[key] = value
    return dictionary


def prompt(message, default=None):
    """Prompt the user for a value. Apply a default value if the user enters
    empty string."""
    if default:
        return input('{0} [{1}]: '.format(message, default)) or default
    else:
        return input('{0}: '.format(message))


def get_datetime(day, time):
    """Return a date object for the specified english weekday day and time."""
    # Normalize the english day to lower case.
    day = day.lower()
    # Get the target weekday number.
    day_weekday = WEEK[day]

    # Get today's date.
    today = datetime.date.today()
    # Get today's weekday number.
    today_weekday = NOW.weekday()

    target = None
    # The target day is today if days match and it is before the target time.
    if day_weekday == today_weekday and NOW.time() < time:
        target = today
    elif day_weekday > today_weekday:
        # The target date is still this week, increment to that day.
        target = today + timedelta(days=day_weekday - today_weekday)
    else:
        # The target date is next week, calculate how many days until that day.
        target = today + timedelta(days=7 - (today_weekday - day_weekday))

    # Combine the hour with the date to get a full time and date.
    return datetime.datetime.combine(target, time)


def get_template(day):
    """Get template for the specified day by name, an exception is thrown
    if the file does not exist for the day specified."""
    template_file = 'templates/{0}'.format(day.lower())
    with open(template_file, 'r') as template_data:
        template_string = template_data.read()
    return template_string


def get_weather(key, location, target_date):
    """Return the forcast and astronomy data using the Weather Underground
    API key, location and target date."""
    astronomy_url = 'http://api.wunderground.com/api/{0}/astronomy/q/{1}.json'
    astronomy_data = {}
    try:
        # Get the astronomy data for the location.
        response = requests.get(astronomy_url.format(key, location))
        if response.status_code != 200:
            message = 'The HTTP response code was not OK for {0}'
            raise ValueError(message.format(astronomy_url))
        if DEBUG:
            date = NOW.strftime('%Y-%m-%d')
            file_name = 'examples/{0}-astronomy.json'.format(date)
            with open(file_name, 'w') as fw:
                print('Writing {0}'.format(file_name))
                fw.write(response.text)
        if 'sun_phase' in response.json():
            astronomy_data = response.json()
        else:
            raise ValueError('The astronomy data does not contain sun_phase!')
    except:
        print('An error occurred getting astronomy data.')
        print(traceback.print_exc())

    hourly10_url = 'http://api.wunderground.com/api/{0}/hourly10day/q/{1}.json'
    hourly10day_data = {}
    try:
        response = requests.get(hourly10_url.format(key, location))
        if response.status_code != 200:
            message = 'The HTTP response code was not OK for {0}'
            raise ValueError(message.format(hourly10_url))
        if DEBUG:
            date = NOW.strftime('%Y-%m-%d')
            file_name = 'examples/{0}-hourly10day.json'.format(date)
            with open(file_name, 'w') as fw:
                print('Writing {0}'.format(file_name))
                fw.write(response.text)
        if 'hourly_forecast' in response.json():
            hourly10day_data = response.json()
        else:
            raise ValueError('The hourly data does not contain hourly_forecast!')
    except:
        print('An error occurred getting the hourly10day data.')
        print(traceback.print_exc())

    return astronomy_data, hourly10day_data


def update_context(context, target_datetime, astronomy_data, hourly10day_data):
    """Update context with the weather data for the target date and time."""
    context['event_time'] = target_datetime.time().strftime('%l:%M %p')
    context['event_date'] = target_datetime.strftime('%B %d, %Y')
    context['event_day'] = target_datetime.strftime('%A')
    # Create a time object with the sunset hour and minute.
    sunset = time(int(astronomy_data['sun_phase']['sunset']['hour']),
                  int(astronomy_data['sun_phase']['sunset']['minute']))
    context['sunset_time'] = sunset.strftime('%l:%M %p')
    # When the sunset is after the target time calculate how the daylight.
    if sunset >= target_datetime.time():
        delta = datetime.datetime.combine(date.today(), sunset) - \
                datetime.datetime.combine(date.today(), target_datetime.time())
        seconds = delta.total_seconds()
        context['daylight_in_seconds'] = seconds
        # Calculate the daylight in minutes.
        context['daylight_in_minutes'] = seconds / 60
        # Calculate the hours of daylight.
        context['daylight_in_hours'] = seconds / 60 / 60
    else:
        context['daylight_in_seconds'] = 0
        context['daylight_in_minutes'] = 0
        context['daylight_in_hours'] = 0

    # Iterate over the entire hourly_forcast array.
    for a in range(0, len(hourly10day_data['hourly_forecast'])):
        forecast = hourly10day_data['hourly_forecast'][a]
        forecast_time = forecast['FCTTIME']
        # Use the record that matches the day and hour.
        if forecast_time['mday'] == str(target_datetime.day) and \
           forecast_time['hour'] == str(target_datetime.hour):
            # Get the values for this matching time and day.
            context['condition'] = forecast['condition']
            context['dewpoint_english'] = forecast['dewpoint']['english']
            context['dewpoint_metric'] = forecast['dewpoint']['metric']
            context['feelslike_english'] = forecast['feelslike']['english']
            context['feelslike_metric']  = forecast['feelslike']['metric']
            context['forecast_time_date'] = forecast_time['pretty']
            context['heatindex_english'] = forecast['heatindex']['english']
            context['heatindex_metric'] = forecast['heatindex']['metric']
            context['humidity'] = forecast['humidity']
            # mslp = mean sea-level pressure, the barometric pressure reduced
            # to sea level.
            context['mean_sea_level_pressure'] = forecast['mslp']
            # Sky is the percent of cloud cover 100 is cloudy, 50 is partially.
            context['percent_cloud_cover'] = forecast['sky']
            # POP stands for Probability of Precipitation. Probability of
            # precipitation refers to the percent chance that a specific
            # location will receive measurable precipitation.
            context['probability_of_precipitation'] = forecast['pop']
            # qpf = Quantitative precipitation forecast.
            context['quantitative_precipitation'] = forecast['qpf']
            context['snow_english'] = forecast['snow']['english']
            context['snow_metric'] = forecast['snow']['metric']
            context['temperature_english'] = forecast['temp']['english']
            context['temperature_metric'] = forecast['temp']['metric']
            context['ultraviolet_index'] = forecast['uvi']
            # wx is the weather condition.
            context['weather_condition'] = forecast['wx']
            context['wind_speed_english'] = forecast['wspd']['english']
            context['wind_speed_metric'] = forecast['wspd']['metric']
            context['wind_direction'] = forecast['wdir']['dir']
            context['wind_degrees'] = forecast['wdir']['degrees']
            context['windchill_english'] = forecast['windchill']['english']
            context['windchill_metric'] = forecast['windchill']['metric']
            break

    return context


def schedule_event(context, day, key, location, time):
    """Use the key to retrieve the weather information for the specified day
    and return the appropriate template using the context."""
    # Get the datetime object for the target day and time.
    target = get_datetime(day, time)
    # Call the Weather Underground API to get the JSON data for the date.
    astronomy_data, hourly10day_data = get_weather(key, location, target)
    # Read the template based on day name, and return as a string.
    template_string = get_template(day)
    # Create the jinja2 object that will replace the variables in the template.
    template = Template(template_string)
    # Update the context with the target date and API data.
    context = update_context(context, target, astronomy_data, hourly10day_data)
    context['location'] = location
    # Replace the template variables with the context values.
    return template.render(context)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        command_line()
    else:
        interactive()
