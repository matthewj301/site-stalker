from pathlib import Path

import requests
from loguru import logger
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

from state_abbreviations import us_state_abbrev

from cachetools import cached


class VaccineSpotter:
    def __init__(self, config, content_dir=None):
        self.available_appointments = dict()
        self.root_dir = Path(__file__).resolve().parent.parent
        if content_dir:
            self.content_dir = Path(content_dir)
        else:
            self.content_dir = self.root_dir.joinpath('content')
        self.vaccine_api_endpoint = 'https://www.vaccinespotter.org/api/v0/states'
        self.config = config['vaccine_watch']
        self.session = requests.session()
        self.state = self.config['state'].upper()
        self.zip_code = str(self.config['zip_code'])
        self.geocoder = Nominatim(user_agent='SiteStalker')
        self.user_lat_long = (self.geocoder.geocode(self.zip_code).latitude,
                              self.geocoder.geocode(self.zip_code).longitude)
        self.acceptable_distance_from_user = self.config['mile_radius']
        if len(self.state) > 2:
            self.state = us_state_abbrev[self.state.lower()]

    def _log(self, _level, msg):
        static_info = 'audit=site_stalker '
        logger.log(_level.upper(), static_info + msg)

    @logger.catch
    @cached(cache={})
    def calculate_site_distance_from_user(self, vax_site_zip_code):
        vax_site_lat_long = (self.geocoder.geocode(vax_site_zip_code).latitude,
                             self.geocoder.geocode(vax_site_zip_code).longitude)
        site_distance = geodesic(self.user_lat_long, vax_site_lat_long).miles
        self._log('info', f'event=calculating_distance_from_user site_zip={vax_site_zip_code}'
                          f' vax_site_lat_long_calculation_result="{str(site_distance)} miles"')
        return site_distance

    @logger.catch
    def download_state_vaccine_data(self):
        req = self.session.get(f'{self.vaccine_api_endpoint}/{self.state}.json')
        if req.status_code < 300:
            self._log('info', 'action=downloading_vaccine_availability_data event=data_retrieved')
            json_data = req.json()['features']
            return json_data
        else:
            self._log('error', f'action=downloading_vaccine_availability_data event=data_not_retrieved '
                               f'status_code={req.status_code} text="{req.text}"')
            return {}

    @logger.catch
    def clean_vaccine_data(self, _json_payload):
        cleaned_site_data = list()
        for _data in _json_payload:
            site_properties = _data['properties']
            if site_properties['postal_code'] is None:
                continue
            cleaned_city = site_properties['city'].lower()
            vax_site_distance = self.calculate_site_distance_from_user(site_properties['postal_code'])
            if vax_site_distance:
                if vax_site_distance <= self.acceptable_distance_from_user:
                    cleaned_site_data.append(
                        {
                            'provider_name': site_properties['provider_brand_name'].lower(),
                            'site_name': site_properties['name'].lower(),
                            'address': f'{site_properties["address"].lower()}, '
                                       f'{cleaned_city}, {self.state},'
                                       f' {site_properties["postal_code"]}',
                            'site_distance': vax_site_distance,
                            'provider_location_id': site_properties['provider_location_id'],
                            'url': site_properties['url'],
                            'appointments': site_properties['appointments']
                        }
                    )
        return cleaned_site_data

    @logger.catch
    def find_vaccine_appointments(self):
        self.available_appointments = dict()
        _site_data = self.clean_vaccine_data(self.download_state_vaccine_data())
        if _site_data:
            for _site in _site_data:
                self.find_vaccine_appointment(_site)
        else:
            self._log('error', f'action=look_for_appointments event=site_data_download_empty '
                               f'reason=connection_reset_or_no_vaccine_locations_in_mile_radius ')
        if not self.available_appointments:
            self._log('warning', f'action=look_for_appointments event=appointments_not_found ')

    @logger.catch
    def find_vaccine_appointment(self, vax_site):
        if vax_site['appointments']:
            self._log('success', f'action=look_for_appointments event=appointments_found '
                                 f'provider={vax_site["provider_name"]} address="{vax_site["address"]}" '
                                 f'distance={vax_site["site_distance"]}')
            if vax_site['provider_name'] not in self.available_appointments:
                self.available_appointments[vax_site['provider_name']] = {'available_apts': len(vax_site['appointments']),
                                                                       'website': vax_site['url']}
            else:
                self.available_appointments[vax_site['provider_name']]['available_apts'] += len(vax_site['appointments'])