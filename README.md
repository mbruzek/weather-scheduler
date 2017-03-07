# Weather Scheduler

An automated solution for scheduling events based on the weather.

## Problem
The local bicycle club has weekly rides on Monday and Wednesday night. Each
day before the ride someone looks up the wind direction, wind speed,
temperature and sunset time to schedule the rides. Scheduling the weekly group
rides is a manual task that takes a human time to complete each week.

## Solution
Create an automated script that can gather the on-line information,
compute the route and post the ride.

## Information

**Requirements**: Must be easier than performing the tasks manually.

**Budget**: Zero dollars.

# Usage

The program can be run on the command line without any flags and will prompt
the user for the options.

```
./weather_scheduler.py
```

If you know the options you want you can call the program with the flags.

```
./weather_scheduler.py -d monday -t '6:00 PM' -k WU_KEY -l MN/Rochester -c "comment=It is getting dark fast so bring a light.,footer=Ride safe."

./weather_scheduler.py -d wednesday -t '6:00 PM' -k WU_KEY -l MN/Rochester -c "comment=It is getting dark fast so bring a light.,footer=Ride safe."
```
