import pytest
import requests

'''
# response = requests.get('https://jsonplaceholder.typicode.com/posts', verify=False)
response = requests.get('https://jsonplaceholder.typicode.com/posts/100', verify=False)

print("\n----------------- text ------------------")
print(response.text)

print("\n----------------- json ------------------")
print(response.json())
'''

base_url_list = [
    'https://jsonplaceholder.typicode.com/posts',
    'https://jsonplaceholder.typicode.com/posts/1',
    'https://jsonplaceholder.typicode.com/posts?userId=1',
    'https://jsonplaceholder.typicode.com/posts/1/comments',
    'https://jsonplaceholder.typicode.com/albums/1/photos',
    'https://jsonplaceholder.typicode.com/users/1/albums',
    'https://jsonplaceholder.typicode.com/users/1/todos',
    'https://jsonplaceholder.typicode.com/users/1/posts'
]
resource_delete_number_list, \
resource_put_number_list = list(range(1, 101)), list(range(1, 101))


@pytest.mark.parametrize("base_url", base_url_list)
def test_json_status(base_url):
    response = requests.get(base_url, verify=False)
    assert response.status_code == 200


def test_json_post():
    headers = {
        'Content-type': 'application/json; charset=UTF-8'
    }
    json = {
        'title': 'foo',
        'body': 'bar',
        'userId': 1
    }
    response = requests.post('https://jsonplaceholder.typicode.com/posts', json=json, headers=headers, verify=False)
    assert response.status_code == 201
    assert response.json()['title'] == 'foo'
    assert response.json()['body'] == 'bar'
    assert response.json()['userId'] == 1
    assert response.json()['id'] == 101


@pytest.mark.parametrize("resource_number", resource_put_number_list)
def test_json_put(resource_number):
    headers = {
        'Content-type': 'application/json; charset=UTF-8'
    }
    json = {
        'id': 1,
        'title': 'foo',
        'body': 'bar',
        'userId': 1
    }
    response = requests.put(f'https://jsonplaceholder.typicode.com/posts/{resource_number}', json=json, headers=headers,
                            verify=False)
    assert response.status_code == 200
    assert response.json()['title'] == 'foo'
    assert response.json()['body'] == 'bar'
    assert response.json()['userId'] == 1
    assert response.json()['id'] == resource_number


def test_json_patch():
    headers = {
        'Content-type': 'application/json; charset=UTF-8'
    }
    json = {
        'title': 'foo'
    }
    response = requests.patch(f'https://jsonplaceholder.typicode.com/posts/1', json=json,
                              headers=headers, verify=False)
    response_get = requests.get(f'https://jsonplaceholder.typicode.com/posts/1', verify=False)
    assert response.status_code == 200
    assert response.json()['title'] == 'foo'
    assert response.json()['body'] == response_get.json()['body']
    assert response.json()['userId'] == 1
    assert response.json()['id'] == 1


@pytest.mark.parametrize("resource_number", resource_delete_number_list)
def test_json_delete(resource_number):
    response = requests.delete(f'https://jsonplaceholder.typicode.com/posts/{resource_number}', verify=False)
    assert response.status_code == 200
