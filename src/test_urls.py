import pytest
import requests


def test_url_status(base_url, base_status_code):
    response = requests.get(base_url, verify=False)
    assert response.status_code == int(base_status_code)
