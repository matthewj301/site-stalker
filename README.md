# SiteStalker

Project to monitor and alert on a website changing between pulls. Also now a covid-19 vaccine appointment finder. 

Original idea
from: https://medium.com/swlh/tutorial-creating-a-webpage-monitor-using-python-and-running-it-on-a-raspberry-pi-df763c142dac

Vaccine Appointment Info from this project's API: https://github.com/GUI/covid-vaccine-spotter 

Note on Twilio: it's free to send yourself text messages, but you will be charged for sending texts to other numbers not
registered to your account.

Note on running this: Podman or Docker should allow you to run this on any OS, but was only tested in Fedora 

# Setup Steps
## Docker/Podman/Environment
1. Install podman or docker on your OS
2. Install git 

## Twilio
1. Set up a Twilio account here: https://www.twilio.com/
2. Find the Twilio account_sid and auth_token in your 'project info' tab, copy this info for later
3. On the Twilio webpage, select 'get a trial number', copy this number for later
   
## Project Setup
1. Download this repo somewhere you want to run it with: git clone https://github.com/matthewj301/site-stalker.git
5. create a file in etc/ called config.yaml, based off of the config.yaml.example file in that same directory
6. fill in the newly-created config.yaml with:
   - The sites to monitor, can be as many as you want
   - Twilio information you saved above including the Twilio-generated phone number
   - Your phone number
   - check_interval, which is the amount of time between checking if a site has changed in seconds
      - Be careful of setting this too low, a site may block your IP if you make too many of the same requests in a period of time
   - other fields relating to enabling or disabling certain features or the radius in miles around your zip to look for vaccine appointments

## Running The Project
### Linux
1. On the commandline in the site-stalker directory, run the following command: podman build -t sitestalker-prod . && podman run --name sitestalker --rm -v $(pwd):/site-stalker --net=host sitestalker-prod:latest
 - This will build the container image and start it up
2. To stop the container run: podman container stop sitestalker
3. To update your config, adjust what you need to in config.yaml, then run: podman restart sitestalker