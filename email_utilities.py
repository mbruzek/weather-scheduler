#!/usr/bin/env python3

"""
email_utilities is Python code to make sending emails easier.

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
import getpass
import os
import smtplib
import sys
import traceback

from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


DESCRIPTION = 'Methods to send an email from a Python program.'
FROM = 'The string email address to send the email from'
IMAGE = 'The string path to the image to attach to the email'
PORT = 'The port to use when connecting to the SMTP server'
PASSWORD = 'The password on the SMTP server'
RECIPIENTS = 'The comma separated email addresses to send the email to'
SERVER = 'The SMTP server to connect with'
SUBJECT = 'The string subject of the email message'
TEXT = 'The main text of the email message'
USERNAME = 'The username to authenticate with the SMTP server'


def command_line():
    """Parse the arguments from the command line."""
    try:
        parser = argparse.ArgumentParser(description=DESCRIPTION)
        parser.add_argument('-f', '--fromaddress',
                            help='{0} [{1}]'.format(FROM, None))
        parser.add_argument('-r', '--recipients',
                            help='{0} [{1}]'.format(RECIPIENTS, None))
        parser.add_argument('--subject',
                            help='{0} [{1}]'.format(SUBJECT, None))
        parser.add_argument('-i', '--image',
                            help='{0} [{1}]'.format(IMAGE, None))
        parser.add_argument('-s', '--server',
                            help='{0} [{1}]'.format(SERVER, None))
        parser.add_argument('--text',
                            help='{0} [{1}]'.format(TEXT, None))
        parser.add_argument('-p', '--port', type=int,
                            help='{0} [{1}]'.format(PORT, None))
        parser.add_argument('-u', '--username',
                            help='{0} [{1}]'.format(USERNAME, None))
        arguments, extra = parser.parse_known_args()

        message = get_message(arguments.fromaddress,
                              arguments.recipients,
                              arguments.subject,
                              arguments.text,
                              arguments.image)

        password = getpass.getpass(PASSWORD + ': ')

        send_tls_message(arguments.server,
                         arguments.port,
                         arguments.username,
                         password,
                         message)
    except:
        print('An error occurred parsing the command-line arguments.')
        print(traceback.print_exc())
        exit(2)


def get_message(from_address, recipients, subject, text, image):
    """Return a MIME message with both text and image parts.
    :param str from_address: The string email address to send from.
    :param list recipients: The comma separated addresses to send the email to.
    :param str subject: The string subject of the email message.
    :param str text: The main path to the text file, or the text itself.
    :param str image: The string path to a MIME supported image file."""
    # Create a MIME multipart message of text and image.
    message = MIMEMultipart()
    message['Subject'] = subject
    message['From'] = from_address
    message['To'] = recipients

    if os.path.isfile(text):
        with open(text, 'r') as reader:
            # Create a MIME text object from the contents of the file.
            content = MIMEText(reader.read())
    else:
        # Create a MIME text message object from the text string.
        content = MIMEText(text)
    # Attach the MIMEText to the MIMEMultipart message.
    message.attach(content)
    if image and os.path.isfile(image):
        # Read the image as binary date from the path.
        with open(image, 'rb') as reader:
            # Create a MIME image message object that contains the raw image.
            mime_image = MIMEImage(reader.read())
            # Attach the MIMEImage to the MIMEMultipart message.
            message.attach(mime_image)
    return message


def interactive(text=None):
    """Prompt the user for the information and send an email message."""
    from_address = prompt(FROM)
    to = prompt(RECIPIENTS)
    subject = prompt(SUBJECT)
    if not text:
        text = prompt(TEXT)
    image_path = prompt(IMAGE)
    message = get_message(from_address, to, subject, text, image_path)

    server = prompt(SERVER, 'smtp.gmail.com')
    port = prompt(PORT, 587)
    username = prompt(USERNAME, from_address)
    password = getpass.getpass(PASSWORD + ": ")
    send_tls_message(server, port, username, password, message)


def prompt(text, default=None):
    """Prompt the user and get input from the standard in."""
    if default:
        return input('{0} [{1}]: '.format(text, str(default))) or default
    else:
        return input('{0}: '.format(text))


def send_tls_message(server, port, username, password, message):
    """Connect to a server on a port, with a username and password to send a
    message."""
    try:
        with smtplib.SMTP(server, port) as email_server:
            email_server.ehlo()
            email_server.starttls()
            email_server.ehlo()
            if username and password:
                email_server.login(username, password)
            # Send the MIME message.
            email_server.send_message(message)
            email_server.close()
    except smtplib.SMTPAuthenticationError as sae:
        print('Unable to authenticate and send message.')
        raise
    except:
        print('Unable to send the message')
        raise


if __name__ == '__main__':
    if len(sys.argv) > 1:
        command_line()
    else:
        interactive()
