# Research

The research done for this project.

# Weather API

## Weather Underground
Weather Underground requires an account to be created to use their API.
https://www.wunderground.com/weather/api/

Once you create an Weather Underground (WU) account you are provided an API
key.

http://api.wunderground.com/api/WU_KEY/astronomy/q/MN/Rochester.json
Returns the moon phase, sunrise and sunset time for the current day.

http://api.wunderground.com/api/WU_KEY/conditions/q/MN/Rochester.json
Returns the current temperature, weather condition, humidity, wind,
'feels like' temperature, barometric pressure, and visibility.

http://api.wunderground.com/api/WU_KEY/forecast/q/MN/Rochester.json
Returns a summary of the weather for the next 3 days. This includes high and
low temperatures, a string text forecast and the conditions.

http://api.wunderground.com/api/WU_KEY/hourly/q/MN/Rochester.json
Returns an hourly forecast for the next 36 hours immediately following the
API request.

http://api.wunderground.com/api/WU_KEY/hourly10day/q/MN/Rochester.json
Returns an hourly forecast for the next 10 days

### Documentation
https://www.wunderground.com/weather/api/d/docs

# Python

## datetime

The [datetime](https://docs.python.org/3/library/datetime.html) module
supplies classes for manipulating dates and times.

The `datetime.datetime.combine(date, time)` method combines a date and a time
objects to make a datetime object, which is handy for building dates.

## date

A [date](https://docs.python.org/3/library/datetime.html#date-objects) object
represents a date (year, month and day) in an idealized calendar, the current
Gregorian calendar indefinitely extended in both directions.

## time
A [time](https://docs.python.org/3.3/library/datetime.html#time-objects) object
represents a time of day, independent of any particular day and subject to
adjustment via a `tzinfo` object.

`time.strftime(format)` - Return a string representing the time, controlled by
an explicit format string. For a complete list of formatting directives see
[strftime() and strptime() Behavior](https://docs.python.org/3.3/library/datetime.html#strftime-strptime-behavior).

## Jinja2

The code uses the [Jinja2 template](http://jinja.pocoo.org/docs/2.9/) package
to make templates that are readable and easy variable substitution.
