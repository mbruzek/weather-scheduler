# Design

Create a command line tool that can query the weather information needed to
plan the routes.

Weather data needed:
 * temperature
 * wind direction
 * wind speed
 * sunset for location

Gathering this information consumes much of the time. Use weather APIs to
collect this information and return it to the user in formatted text that
can be posted to a forum or pasted in an email.

# Requirements

The tool needs to output text for the event. In general the event postings need
the following information:

Location of event, start time

Weather forcast for the time of the event.

Temperature, wind direction, chance of precipitation.

Sunset time to get an idea of how much daylight is available.

Optional comment.

Image for the event.

Closing statement or footer.

## Templates

Templates are the easiest way to output structured text from an application.
This application uses Jinja2 templates to replace sections of the templates
when the program runs.

All the templates are stored in the `templates` directory and are named for the
day of the week with lowercase letters. The program can load the appropriate
template and replace the variables (mostly from the weather data) before
printing the final text to the standard output. You can customize each day's
templates with different messages so each day has its own message.

```
templates/monday
templates/wednesday
```

### Phase 1

[X] Research the weather APIs to see which one provides what we need. Keep links
to documentation in RESEARCH.md so when the APIs break or more functionality is
needed the information is available.

* Using the astronomy API for sunset time, and the hourly10day API for the
hourly data.

### Phase 2

[X] Implement simple requests to gather the weather information.

* Using the requests Python package to issue simple HTTP GET commands.
* Parsing the JSON is the hardest part, saved JSON in the `examples` directory.

### Phase 3

[X] Make the system work from the command line with replaceable credentials that
are not hard coded.

* Both command line and interactive are supported.

### Phase 4

Look into where to run this tool, likely a Raspberry Pi or something cheap
and low powered that can run for a long time unattended.

### Phase 5

Schedule the tool to run every night and post information to the group/forum or
email.

### Phase6

Release to production, maintain the tool by fixing bugs and adding features.
