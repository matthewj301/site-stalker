import yaml

class UserNotify:
    def __init__(self, config_file):
        self.config = yaml.safe_load(config_file.open())

    def notify_parties(self, txt):
        print(txt)