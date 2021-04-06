#!/usr/bin/env python

from site_stalker.vaccine_spot import VaccineSpotter
from site_stalker.notify import Notifier
from site_stalker.stalk import SiteStalker
from pathlib import Path
import yaml
import pytest

config_dir = Path(__file__).resolve().parent.parent.joinpath('etc/')
config_file = config_dir.joinpath('config.yaml.test').resolve()
config = yaml.safe_load(config_file.open())

test_data_1 = [
    {"type": "Feature", "geometry": {"type": "Point", "coordinates": [-90.339647, 40.946241]},
     "properties": {"id": 14422536, "url": "https://www.hy-vee.com/my-pharmacy/covid-vaccine-consent",
                    "city": "Galesburg", "name": "Galesburg #2", "state": "IL", "address": "2030 E Main St",
                    "provider": "hyvee", "time_zone": "America/Chicago", "postal_code": "60056", "appointments": [],
                    "provider_brand": "hyvee", "carries_vaccine": None, "appointment_types": {"unknown": True},
                    "provider_brand_id": 1338, "provider_brand_name": "Hy-Vee",
                    "provider_location_id": "b0e4269c-e1b4-45e8-bbef-b56554a8f46b", "appointments_available": True,
                    "appointment_vaccine_types": {"unknown": True},
                    "appointments_last_fetched": "2021-04-06T19:50:35.237+00:00",
                    "appointments_last_modified": "2021-04-06T19:50:35.237+00:00",
                    "appointments_available_all_doses": True, "appointments_available_2nd_dose_only": False}}]

test_data_2 = [{"type": "Feature", "geometry": {"type": "Point", "coordinates": [-90.380774, 40.971667]},
                "properties": {"id": 14422532, "url": "https://www.hy-vee.com/my-pharmacy/covid-vaccine-consent",
                               "city": "Galesburg", "name": "Galesburg #1", "state": "IL",
                               "address": "1975 National Boulevard", "provider": "hyvee",
                               "time_zone": "America/Chicago", "postal_code": "61401",
                               "appointments": [{"time": "2021-04-07T15:30:00.000-05:00"},
                                                {"time": "2021-04-08T10:50:00.000-05:00"}],
                               "provider_brand": "hyvee", "carries_vaccine": None,
                               "appointment_types": {"unknown": True}, "provider_brand_id": 1338,
                               "provider_brand_name": "Hy-Vee",
                               "provider_location_id": "8590ef93-c01a-4e71-b0e4-bcf07e5d7af2",
                               "appointments_available": True, "appointment_vaccine_types": {"unknown": True},
                               "appointments_last_fetched": "2021-04-06T19:50:35.237+00:00",
                               "appointments_last_modified": "2021-04-06T19:50:35.237+00:00",
                               "appointments_available_all_doses": True,
                               "appointments_available_2nd_dose_only": False}}]

test_data_3 = [{"type": "Feature", "geometry": {"type": "Point", "coordinates": [-87.923386, 42.069294]},
                "properties": {"id": 783490,
                               "url": "https://www.walmart.com/pharmacy/clinical-services/immunization/scheduled?imzType=covid",
                               "city": "Mount Prospect", "name": "Mount Prospect Supercenter", "state": "IL",
                               "address": "930 Mount Prospect Plz", "provider": "walmart",
                               "time_zone": "America/Chicago", "postal_code": "61401", "appointments": [],
                               "provider_brand": "walmart", "carries_vaccine": True, "appointment_types": {},
                               "provider_brand_id": 70, "provider_brand_name": "Walmart",
                               "provider_location_id": "1681", "appointments_available": False,
                               "appointment_vaccine_types": {},
                               "appointments_last_fetched": "2021-04-06T19:51:09.263+00:00",
                               "appointments_last_modified": "2021-04-06T19:51:09.263+00:00",
                               "appointments_available_all_doses": False,
                               "appointments_available_2nd_dose_only": False}}]

cleaned_data_2 = {'provider_name': 'hy-vee', 'site_name': 'galesburg #1',
                  'address': '1975 national boulevard, galesburg, IL, 61401', 'site_distance': 0.0,
                  'provider_location_id': '8590ef93-c01a-4e71-b0e4-bcf07e5d7af2',
                  'url': 'https://www.hy-vee.com/my-pharmacy/covid-vaccine-consent',
                  'appointments': [{'time': '2021-04-07T15:30:00.000-05:00'},
                                   {'time': '2021-04-08T10:50:00.000-05:00'}]}

cleaned_data_3 = {'provider_name': 'walmart', 'site_name': 'mount prospect supercenter',
                  'address': '930 mount prospect plz, mount prospect, IL, 61401', 'site_distance': 0.0,
                  'provider_location_id': '1681',
                  'url': 'https://www.walmart.com/pharmacy/clinical-services/immunization/scheduled?imzType=covid',
                  'appointments': []}


@pytest.fixture
def vaccine_finder_init():
    return VaccineSpotter(config)


@pytest.fixture
def notifier_init():
    return Notifier(config)


@pytest.fixture
def site_stalker_init():
    return SiteStalker(config)


# def test_vaccine_spotter_api_return(vaccine_finder_init):
#    assert bool(vaccine_finder_init.download_state_vaccine_data()) is True


def test_cleaning_api_data(vaccine_finder_init):
    # These are based off of zipcode in etc/config.yaml.test, I adjusted test_data zips,
    # so they do not match addresses currently

    # This one is out of our 15 mile radius
    test_1_result = vaccine_finder_init.clean_vaccine_data(test_data_1)
    assert bool(test_1_result) is False

    # This one is in radius, with vaccine appointments
    test_2_result = vaccine_finder_init.clean_vaccine_data(test_data_2)
    assert bool(test_2_result) is True

    # This one is in radius, without vaccine appointments
    test_3_result = vaccine_finder_init.clean_vaccine_data(test_data_3)
    assert bool(test_3_result) is True


def test_finding_vaccine_appointment(vaccine_finder_init):
    # This one has vaccine appointments
    assert vaccine_finder_init.find_vaccine_appointment(cleaned_data_2) is True
    # This one does not have vaccine appointments
    assert vaccine_finder_init.find_vaccine_appointment(cleaned_data_3) is False
