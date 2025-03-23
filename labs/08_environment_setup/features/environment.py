"""
Environment for Behave Testing
"""
from os import getenv
from selenium import webdriver

WAIT_SECONDS = int(getenv('WAIT_SECONDS', 60))
BASEURL = getenv('BASE_URL', 'http://localhost:8080')

def before_all(context):
    """ Executed once before all tests """
    context.wait_seconds = WAIT_SECONDS
    context.base_url = BASEURL


def after_all(context):
    """ Executed after all tests """
