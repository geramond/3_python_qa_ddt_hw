import pytest
import requests


def get_breweries_params(source, param):
    names = []
    response = requests.get(f'{source}', verify=False)
    for i in response.json():
        names.append(i[f'{param}'])
    return names


def get_brewery_keys(source):
    response = requests.get(f'{source}', verify=False)
    return list(response.json()[0].keys())


base_url_list = [
    'https://api.openbrewerydb.org/breweries',
    'https://api.openbrewerydb.org/breweries?by_city=san_diego',
    'https://api.openbrewerydb.org/breweries?by_city=san%20diego',
    'https://api.openbrewerydb.org/breweries/search?query=dog',

]
base_url_list_get_brewery_autocomplete = [
    'https://api.openbrewerydb.org/breweries/autocomplete?query=dog',
    'https://api.openbrewerydb.org/breweries/madtree-brewing-cincinnati'

]

brewery_keys = get_brewery_keys('https://api.openbrewerydb.org/breweries')
brewery_keys_autocomplete = get_brewery_keys('https://api.openbrewerydb.org/breweries/autocomplete?query=dog')

brewery_names = get_breweries_params('https://api.openbrewerydb.org/breweries', 'name')
brewery_ids = get_breweries_params('https://api.openbrewerydb.org/breweries', 'id')


@pytest.mark.parametrize("base_url", base_url_list)
def test_brewery_status(base_url):
    response = requests.get(base_url, verify=False)
    assert response.status_code == 200


@pytest.mark.parametrize("base_url", base_url_list)
def test_brewery_keys(base_url):
    response = requests.get(base_url, verify=False)
    for i in response.json():
        assert list(i.keys()) == brewery_keys


def test_get_brewery_autocomplete():
    response = requests.get('https://api.openbrewerydb.org/breweries/autocomplete?query=dog', verify=False)
    assert response.status_code == 200
    for i in response.json():
        assert list(i.keys()) == brewery_keys_autocomplete


def test_brewery_autocomplete_maximum_15_results():
    response = requests.get('https://api.openbrewerydb.org/breweries/autocomplete?query=dog', verify=False)
    assert len(response.json()) <= 15


@pytest.mark.parametrize("brewery_id", brewery_ids)
def test_breweries_status(brewery_id):
    response = requests.get(f'https://api.openbrewerydb.org/breweries/{brewery_id}', verify=False)
    assert response.status_code == 200


@pytest.mark.parametrize("brewery_id", brewery_ids)
def test_breweries_keys(brewery_id):
    response = requests.get(f'https://api.openbrewerydb.org/breweries/{brewery_id}', verify=False)
    assert list(response.json().keys()) == brewery_keys


@pytest.mark.parametrize("brewery_id", brewery_ids)
def test_breweries_names(brewery_id):
    response = requests.get(f'https://api.openbrewerydb.org/breweries/{brewery_id}', verify=False)
    assert response.json()['name'] in brewery_names
