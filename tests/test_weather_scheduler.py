import json
import unittest
import sys
from datetime import datetime
from os import path
# Have to append ../../ to the system path because this test is not a module.
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import weather_scheduler.weather_scheduler as weather_scheduler


ASTRONOMY = '''
{
  "response": {
    "version": "0.1",
    "termsofService": "http://www.wunderground.com/weather/api/d/terms.html",
    "features": {
      "astronomy": 1
    }
  },
  "moon_phase": {
    "percentIlluminated": "100",
    "ageOfMoon": "15",
    "phaseofMoon": "Full",
    "hemisphere": "North",
    "current_time": {
      "hour": "19",
      "minute": "13"
    },
    "sunrise": {
      "hour": "7",
      "minute": "27"
    },
    "sunset": {
      "hour": "19",
      "minute": "12"
    },
    "moonrise": {
      "hour": "19",
      "minute": "29"
    },
    "moonset": {
      "hour": "7",
      "minute": "36"
    }
  },
  "sun_phase": {
    "sunrise": {
      "hour": "7",
      "minute": "27"
    },
    "sunset": {
      "hour": "19",
      "minute": "12"
    }
  }
}
'''
HOURLY_10_DAY = '''
{
  "response": {
    "version": "0.1",
    "termsofService": "http://www.wunderground.com/weather/api/d/terms.html",
    "features": {
      "hourly10day": 1
    }
  },
  "hourly_forecast": [
    {
      "FCTTIME": {
        "hour": "20",
        "hour_padded": "20",
        "min": "00",
        "min_unpadded": "0",
        "sec": "0",
        "year": "2017",
        "mon": "3",
        "mon_padded": "03",
        "mon_abbrev": "Mar",
        "mday": "12",
        "mday_padded": "12",
        "yday": "70",
        "isdst": "1",
        "epoch": "1489366800",
        "pretty": "8:00 PM CDT on March 12, 2017",
        "civil": "8:00 PM",
        "month_name": "March",
        "month_name_abbrev": "Mar",
        "weekday_name": "Sunday",
        "weekday_name_night": "Sunday Night",
        "weekday_name_abbrev": "Sun",
        "weekday_name_unlang": "Sunday",
        "weekday_name_night_unlang": "Sunday Night",
        "ampm": "PM",
        "tz": "",
        "age": "",
        "UTCDATE": ""
      },
      "temp": {
        "english": "20",
        "metric": "-7"
      },
      "dewpoint": {
        "english": "19",
        "metric": "-7"
      },
      "condition": "Snow",
      "icon": "snow",
      "icon_url": "http://icons.wxug.com/i/c/k/nt_snow.gif",
      "fctcode": "21",
      "sky": "100",
      "wspd": {
        "english": "7",
        "metric": "11"
      },
      "wdir": {
        "dir": "ENE",
        "degrees": "76"
      },
      "wx": "Snow",
      "uvi": "0",
      "humidity": "96",
      "windchill": {
        "english": "10",
        "metric": "-12"
      },
      "heatindex": {
        "english": "-9999",
        "metric": "-9999"
      },
      "feelslike": {
        "english": "10",
        "metric": "-12"
      },
      "qpf": {
        "english": "0.03",
        "metric": "1"
      },
      "snow": {
        "english": "0.4",
        "metric": "10"
      },
      "pop": "83",
      "mslp": {
        "english": "30.33",
        "metric": "1027"
      }
    },
    {
      "FCTTIME": {
        "hour": "19",
        "hour_padded": "19",
        "min": "00",
        "min_unpadded": "0",
        "sec": "0",
        "year": "2017",
        "mon": "3",
        "mon_padded": "03",
        "mon_abbrev": "Mar",
        "mday": "22",
        "mday_padded": "22",
        "yday": "80",
        "isdst": "1",
        "epoch": "1490227200",
        "pretty": "7:00 PM CDT on March 22, 2017",
        "civil": "7:00 PM",
        "month_name": "March",
        "month_name_abbrev": "Mar",
        "weekday_name": "Wednesday",
        "weekday_name_night": "Wednesday Night",
        "weekday_name_abbrev": "Wed",
        "weekday_name_unlang": "Wednesday",
        "weekday_name_night_unlang": "Wednesday Night",
        "ampm": "PM",
        "tz": "",
        "age": "",
        "UTCDATE": ""
      },
      "temp": {
        "english": "40",
        "metric": "4"
      },
      "dewpoint": {
        "english": "21",
        "metric": "-6"
      },
      "condition": "Chance of Rain",
      "icon": "chancerain",
      "icon_url": "http://icons.wxug.com/i/c/k/nt_chancerain.gif",
      "fctcode": "12",
      "sky": "70",
      "wspd": {
        "english": "8",
        "metric": "13"
      },
      "wdir": {
        "dir": "SE",
        "degrees": "135"
      },
      "wx": "Showers",
      "uvi": "0",
      "humidity": "45",
      "windchill": {
        "english": "34",
        "metric": "1"
      },
      "heatindex": {
        "english": "-9999",
        "metric": "-9999"
      },
      "feelslike": {
        "english": "34",
        "metric": "1"
      },
      "qpf": {
        "english": "0.02",
        "metric": "1"
      },
      "snow": {
        "english": "0.0",
        "metric": "0"
      },
      "pop": "39",
      "mslp": {
        "english": "30.15",
        "metric": "1021"
      }
    }
  ]
}
'''


class TestWeatherScheduler(unittest.TestCase):
    """A unit test TestCase class to run tests on the main code."""

    def test_split_kv_string(self):
        """Make sure the split_kv_string() method correctly splits strings."""
        kv_string_1 = 'footer=This is the footer.,comment=This is a comment.'
        result = weather_scheduler.split_kv_string(kv_string_1)
        assert 'footer' in result
        assert 'This is the footer.' == result['footer']
        assert 'comment' in result
        assert 'This is a comment.' == result['comment']

    def test_update_context(self):
        """Make sure the update_context() method is correctly parsing json."""
        context = {'test': True}
        target_datetime = datetime(2017, 3, 22, 19, 00)
        astronomy = json.loads(ASTRONOMY)
        hourly10day = json.loads(HOURLY_10_DAY)
        updated = weather_scheduler.update_context(context, target_datetime,
                                                   astronomy, hourly10day)
        assert 'event_time' in updated
        assert ' 7:00 PM' == updated['event_time']
        assert 'event_date' in updated
        assert 'March 22, 2017' == updated['event_date']

        assert 'sunset_time' in updated
        assert ' 7:12 PM' == updated['sunset_time']

        assert 'temperature_english' in updated
        assert '40' == updated['temperature_english']

        assert 'probability_of_precipitation' in updated
        assert '39' == updated['probability_of_precipitation']

        assert 'wind_direction' in updated
        assert 'SE' == updated['wind_direction']
        assert 'wind_speed_english' in updated
        assert '8' == updated['wind_speed_english']
