from setuptools import setup
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name='weather_scheduler',
    version='0.9.0',
    description='Schedule events based on the weather information.',
    long_description="""The weather_scheduler program gets weather information 
        for a specific location, date and time. The weather data can be used in
        event templates that can be emailed to a group of people.""",
    url='https://github.com/mbruzek/weather-scheduler',
    author='Matthew Bruzek',
    author_email='mbruzek@gmail.com',
    keywords='python weather schedule recurring email event',
    packages=['weather_scheduler', 'email_utilities'],
    install_requires=['Jinja2', 'requests'],
    extras_require={'test': ['pytest']},
    project_urls={
        'Bug Reports': 'https://github.com/mbruzek/weather-scheduler/issues',
        'Source': 'https://github.com/mbruzek/weather-scheduler',
    }
)
