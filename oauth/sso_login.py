from selenium import webdriver
from credentials import client_id, redirect_uri, OAUTH_URL
import re

from utils import PROJECT_ROOT
from .request import UserFieldAPIRequest
from selenium.common.exceptions import WebDriverException
from server.bottle_server import start_server, stop_server
import os
from .exceptions import InvalidLoginError
import sys
from uuid import uuid4

access_token_regex = re.compile(r'access_token=([^&]*)')
state_regex = re.compile(r'state=([^&]*)')

roll_no_file = os.path.join(PROJECT_ROOT, './data/roll_no_list.txt')


def login():

    # Validate if roll_no_file is present
    if not os.path.isfile(roll_no_file):
        raise ValueError('Invalid configuration. Contact system administrator')

    sys.stdout.write('Initializing Login Sequence...\n')
    start_server()
    sys.stdout.write('Loading SSO Login protocol...\n')
    profile = webdriver.FirefoxProfile()
    profile.set_preference('network.proxy.type', 0)
    driver = webdriver.Firefox(profile)
    sys.stdout.write('SSO Login protocol loaded\n')

    request_state = uuid4().hex
    sso_url = '%s?client_id=%s&response_type=token&scope=basic profile ldap program&state=%s' % (
        OAUTH_URL, client_id, request_state)
    driver.get(sso_url)

    while True:
        try:
            current_url = driver.current_url
            if current_url.startswith(redirect_uri):
                break
        except WebDriverException:
            return None, False
    driver.close()
    stop_server()
    sys.stdout.write('Login Sequence Finished\n\n')

    # Validate State
    state = state_regex.findall(current_url)
    if len(state) == 0:
        return None, False
    state = state[0]
    if state != request_state:
        return None, False

    access_token = access_token_regex.findall(current_url)
    if len(access_token) == 0:
        return None, False
    access_token = access_token[0]
    user_request = UserFieldAPIRequest(access_token=access_token)
    sys.stdout.write('Fetching User Information...\n')
    user = user_request.get_oauth_user()
    sys.stdout.write('Received User Information\n')
    roll_no = user.roll_number
    is_alumni = user.is_alumni
    type_ = user.type
    if is_alumni:
        raise InvalidLoginError(title='Invalid Credentials', message='Alumni Account')
    if type_ not in ['ug', 'pg', 'dd', 'rs']:
        raise InvalidLoginError(title='Invalid Credentials', message='Not a Student Account')

    mess_member = False
    with open(roll_no_file, 'r') as mess_member_list:
        for line in mess_member_list:
            if roll_no in line:
                mess_member = True
                break
    if not mess_member:
        raise InvalidLoginError(title='Invalid credentials', message='Not a Member of the Hostel Mess')

    return roll_no, True
