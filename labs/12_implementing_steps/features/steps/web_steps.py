# pylint: disable=function-redefined, missing-function-docstring
# flake8: noqa
"""
Web Steps
Steps file for web interactions with Selenium
For information on Waiting until elements are present in the HTML see:
    https://selenium-python.readthedocs.io/waits.html
"""

from behave import given, when, then
from selenium.webdriver.common.by import By

@given('I am on the "Home Page"')
def step_impl(context):
    context.response = context.driver.get(context.base_url)


@when('I set the "Category" to "{pet_name}"')
def step_impl(context, pet_name):
    element = context.driver.find_element(By.ID, 'pet_category')
    element.clear()
    element.send_keys(pet_name)


@when('I click the "Search" button')
def step_impl(context):
    element = context.driver.find_element(By.ID, 'search-btn')
    element.click()


@then('I should see the message "{message}"')
def step_impl(context, message):
    message = message.lower().replace(' ', '_')
    element = context.driver.find_element(By.ID, 'flash_message')
    assert message in element.text


@then('I should see "{pet_name}" in the results')
def step_impl(context, pet_name):
    element = context.driver.find_element(By.ID, 'search_results')
    assert pet_name in element.text


@then('I should not see "{pet_name}" in the results')
def step_impl(context, pet_name):
    element = context.driver.find_element(By.ID, 'search_results')
    assert pet_name not in element.text
