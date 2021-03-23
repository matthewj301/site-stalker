from twilio.rest import Client


class Notifier:
    def __init__(self, config):
        self.config = config
        self.twilio_account_sid = self.config['twilio']['account_sid']
        self.twilio_auth_token = self.config['twilio']['auth_token']
        self.twilio_phone_number = self.clean_phone_number(self.config['twilio']['twilio_phone_number'])
        self.user_phone_number = self.clean_phone_number(self.config['twilio']['user_phone_number'])

    def clean_phone_number(self, phone_number):
        phone_number = str(phone_number)
        if isinstance(phone_number, str):
            if '-' in phone_number:
                phone_number = ''.join(phone_number.split('-'))
            if phone_number[0] != '1':
                phone_number = '1' + phone_number
            if '+' not in phone_number:
                phone_number = '+' + phone_number
        return phone_number

    def send_text_msg(self, txt):
        client = Client(self.twilio_account_sid, self.twilio_auth_token)
        client.messages.create(to=self.user_phone_number,
                               from_=self.twilio_phone_number,
                               body=txt)

    def format_site_change_notification(self, _site):
        formatted_msg = f'The site {_site} changed from last check. URL: {self.config["sites"][_site]}'
        return formatted_msg

    def format_vaccine_availability_notification(self, vaccine_apt_dict):
        final_msg_list = list()
        for _provider, _info in vaccine_apt_dict.items():
            formatted_msg = f'Appointments Open at {_provider} | ' \
                            f'# of apts: {_info["available_apts"]} | website: {_info["website"]}'
            final_msg_list.append(formatted_msg)
        return '\n'.join(final_msg_list)

    def notify_user_of_site_change(self, _site):
        txt_msg = self.format_site_change_notification(_site)
        self.send_text_msg(txt_msg)

    def notify_user_of_vaccine(self, vaccine_apt_dict):
        formatted_sms = self.format_vaccine_availability_notification(vaccine_apt_dict)
        self.send_text_msg(formatted_sms)