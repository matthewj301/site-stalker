# site_stalker
Project to monitor and alert on a website changing between pulls

Original idea from: https://medium.com/swlh/tutorial-creating-a-webpage-monitor-using-python-and-running-it-on-a-raspberry-pi-df763c142dac

Note on Twilio: it's free to send yourself text messages, but you will be charged for sending texts to other numbers not registered to your account.
## Setup Steps
1. Download this repo somewhere you want to run it with: git clone https://github.com/matthewj301/site_stalker.git
2. Set up a Twilio account here: https://www.twilio.com/
3. Find the Twilio account_sid and auth_token in your 'project info' tab, copy this info for later
4. On the Twilio webpage, select 'get a trial number', copy this number  for later
5. create a file in etc/ called config.yaml, based off of the config.yaml.example file in that same directory
6. fill in the newly-created config.yaml with the sites to monitor, as well as the twilio information you saved above
