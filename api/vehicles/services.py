import logging
import requests


def __get_data_from_vehicles_api():
    response = requests.get("https://raw.githubusercontent.com/chargeprice/open-ev-data/master/data/ev-data.json")
    if response.status_code == 200:
        return response.json()
    else:
        logging.error("Error getting data from API")
        return None

def get_data_vehicles():
    data = __get_data_from_vehicles_api()
    if data is not None:
        pass
    return data