import requests


def get_list_of_zip_codes(state, city):
    key = "IonBf0AnrfmEfzHNBtjvJ53DsZmVV3eDrBeHCP435rIk0q7BUr7DwbhYaDU5H8J8"
    url = "https://www.zipcodeapi.com/rest/{key}/city-zips.json/{city}/{state}".format(state=state, city=city, key=key)
    resp = requests.get(url)
    assert resp.status_code == 200, "zipcodeapi.com return not 200"
    return resp.json()['zip_codes']
