# pylint: disable=function-redefined, missing-function-docstring
# flake8: noqa
"""
Pet Steps
Steps file for Pet.feature
For information on Waiting until elements are present in the HTML see:
    https://selenium-python.readthedocs.io/waits.html
"""
import requests
from behave import given

@given('the following pets')
def step_impl(context):
    """Load the pets into the database"""

    # Delete existing pets
    response = requests.get(f"{context.base_url}/pets")
    assert response.status_code == 200

    for pet in response.json():
        response_to_delete = requests.delete(f"{context.base_url}/pets/{pet['id']}")
        assert response_to_delete.status_code == 204

    # Load the new pets
    for row in context.table:
        payload = {
            'name': row['name'],
            'category': row['category'],
            'available': row['available'],
            'gender': row['gender'],
            'birthdate': row['birthdate']
        }

    response = requests.post(f"{context.base_url}/pets", json=payload)
    assert context.response.status_code == 201
