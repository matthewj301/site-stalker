# SiteStalker

Project to monitor and alert on a website changing between pulls. Also now a covid-19 vaccine appointment finder. 

Original idea
from: https://medium.com/swlh/tutorial-creating-a-webpage-monitor-using-python-and-running-it-on-a-raspberry-pi-df763c142dac

Vaccine Appointment Info from this project's API: https://github.com/GUI/covid-vaccine-spotter 

Note on Twilio: it's free to send yourself text messages, but you will be charged for sending texts to other numbers not
registered to your account.

Note on running this: Podman or Docker should allow you to run this on any OS, but was only tested in Fedora and RaspberryPiOS

# Setup Steps
## Docker/Podman/Environment
1. Install podman or docker on your OS
2. Install git (if you need to build the container yourself)

## Twilio
1. Set up a Twilio account here: https://www.twilio.com/
2. Find the Twilio account_sid and auth_token in your 'project info' tab, copy this info for later
3. On the Twilio webpage, select 'get a trial number', copy this number for later
   
## Project Setup
1. Download and edit this config file, name it config.yaml https://github.com/matthewj301/site-stalker/blob/main/etc/config.yaml.example
   - This can be saved anywhere, as long as the path won't change, since we will just pass the docker container a path to the config file
2. fill in the newly-created config.yaml with:
   - The sites to monitor, can be as many as you want
   - Twilio information you saved above including the Twilio-generated phone number
   - Your phone number
   - check_interval, which is the amount of time between checking if a site has changed in seconds
      - Be careful of setting this too low, a site may block your IP if you make too many of the same requests in a period of time
   - other fields relating to enabling or disabling certain features or the radius in miles around your zip to look for vaccine appointments

## Running The Project
### Linux
1. the docker container (hosted at https://hub.docker.com/repository/docker/matthewj301/sitestalker) with the 'latest' tag supports linux/amd64, linux/arm64, linux/arm/v6, and linux/arm/v7
   1. Run this command to download and start the container: podman run --name sitestalker-<unique_name_if_multiple_being_spun_up> -v /path/to/local/config.yaml:/etc/config.yaml -v /etc/localtime:/etc/localtime:ro --net=host matthewj301/sitestalker:<tag_you_found>
     - Note: if you are not running this in Linux, you may have to adjust the '-v /etc/localtime:/etc/localtime:ro' portion of the run command, or you can just remove it if you don't care about the logs being in your local timezone
2. If you don't find one, do the following
   1. podman build -t sitestalker .
   2. podman run --name sitestalker-<unique_name_if_multiple_being_spun_up> -v /path/to/local/config.yaml:/etc/config.yaml -v /etc/localtime:/etc/localtime:ro --net=host sitestalker
     - Note: if you are not running this in Linux, you may have to adjust the '-v /etc/localtime:/etc/localtime:ro' portion of the run command, or you can just remove it if you don't care about the logs being in your local timezone
3. To stop the container run: podman container stop sitestalker-<unique_name_if_multiple_being_spun_up>
4. To update your config, adjust what you need to in config.yaml, then run: podman restart sitestalker-<unique_name_if_multiple_being_spun_up>
