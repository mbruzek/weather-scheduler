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

The tool needs to output text for the ride. In general the ride postings look
like this:

Day of week, date, Location of start, time.

Common information about the groups and depart times.

Forecast temperature, wind direction, wind speed. Sunset time.

Optional comments to bring lights or be safe on trails


## Templates

The easiest way to output formatted text. Use jinja2 templates to make sections
of the templates replaceable.

It looks like templates based on the day of week is needed. The algorithm can
load the appropriate template and replace the weather variables.

monday.txt
wednesday.txt

## Phase 1

Research the weather APIs to see which one provides what we need. Keep links
to documentation in RESEARCH.md so when the APIs break or more functionality is
needed the information is available.

## Phase 2

Implement simple requests to gather the weather information.

## Phase 3

Make the system work from the command line with replaceable credentials that
are not hard coded.

## Phase 4

Look into where to run this tool, likely a Raspberry Pi or something cheap
and low powered that can run for a long time unattended.

## Phase 5

Schedule the tool to run every night and post information to the group/forum or
email.

## Phase6

Release to production, maintain the tool by fixing bugs and adding features.
