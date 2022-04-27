import pytest
import requests


def get_breeds_keys(source):
    response = requests.get(f'{source}', verify=False)
    return list(response.json()['message'].keys())


breeds_list = get_breeds_keys('https://dog.ceo/api/breeds/list/all')
base_url_list = [
    'https://dog.ceo/api/breeds/list/all',
    'https://dog.ceo/api/breeds/image/random',
    'https://dog.ceo/api/breed/hound/images',
    'https://dog.ceo/api/breed/hound/images/random',
    'https://dog.ceo/api/breed/hound/images/random/3',
    'https://dog.ceo/api/breed/hound/list',
    'https://dog.ceo/api/breed/hound/afghan/images/random',
    'https://dog.ceo/api/breed/hound/afghan/images/random/3'

]
multiple_collection_url_list = [
    'https://dog.ceo/api/breed/hound/images/random/3',
    'https://dog.ceo/api/breed/hound/afghan/images/random/3'
]
amount_list = list(range(1, 101))


@pytest.mark.parametrize("base_url", base_url_list)
def test_breeds_status(base_url):
    response = requests.get(base_url, verify=False)
    assert response.status_code == 200
    assert response.json().get("status") == "success"


@pytest.mark.parametrize("amount", amount_list)
def test_breeds(amount):
    response = requests.get(f'https://dog.ceo/api/breeds/image/random/{amount}', verify=False)
    assert len(response.json()['message']) <= 50


def test_sub_breeds_():
    response = requests.get('https://dog.ceo/api/breed/hound/list', verify=False)
    assert len(response.json().get('message')) == 7
    assert response.json().get('message') == ['afghan', 'basset', 'blood', 'english', 'ibizan', 'plott', 'walker']


@pytest.mark.parametrize("base_url", multiple_collection_url_list)
def test_multiple_breeds_count(base_url):
    response = requests.get(base_url, verify=False)
    assert len(response.json().get('message')) == 3


@pytest.mark.parametrize("breed_name", breeds_list)
def test_breeds_random(breed_name):
    response = requests.get(f"https://dog.ceo/api/breed/{breed_name}/images/random", verify=False)
    assert response.status_code == 200
