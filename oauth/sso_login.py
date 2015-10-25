from selenium import webdriver
from credentials import client_id, redirect_uri, OAUTH_URL
import re
from .request import UserFieldAPIRequest
from selenium.common.exceptions import WebDriverException
from server.bottle_server import start_server, stop_server


access_token_regex = re.compile(r'access_token=([^&]*)')


def login():
    start_server()
    profile = webdriver.FirefoxProfile()
    profile.set_preference('network.proxy.type', 0)
    driver = webdriver.Firefox(profile)
    sso_url = '%s?client_id=%s&response_type=token&scope=basic ldap program' % (OAUTH_URL, client_id)
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
    access_token = access_token_regex.findall(current_url)
    if len(access_token) == 0:
        return None, False
    access_token = access_token[0]
    user_request = UserFieldAPIRequest(access_token=access_token)
    user = user_request.get_oauth_user()
    return user.username, True

