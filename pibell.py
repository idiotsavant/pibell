#!/usr/bin/python

import RPi.GPIO as GPIO
import httplib
import urllib
from time import sleep

# Set GPIO pin numbering scheme to BCM
GPIO.setmode(GPIO.BCM)

# Set GPIO pin to input, set it to pull up (as we are monitoring difference to ground)
GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Endless loop
while True:

    # Wait for interrupt
    print 'Waiting for doorbell...'
    GPIO.wait_for_edge(25, GPIO.FALLING)

    # Notify using Pushover
    print 'Sending notification'
    conn = httplib.HTTPSConnection("api.pushover.net:443")
    conn.request("POST",
                 "/1/messages.json",
                 urllib.urlencode({
                                  "token": "YOUR_APP_TOKEN_HERE",
                                  "user": "YOUR_USER_KEY_HERE",
                                  "title": "Doorbell!",
                                  "message": "Somebody just rang the doorbell",
                                  }),
                 {"Content-type": "application/x-www-form-urlencoded"})
    response = conn.getresponse()
    print 'Status ' + response.status + ': ' + response.reason

    # Wait 10 seconds so doorbell press(es) end
    sleep(10)

# Clean up GPIO on exit
GPIO.cleanup()
