class OAuthError(Exception):

    def __init__(self, message=None, response=None):
        super(OAuthError, self).__init__(message)
        self.response = response


class InvalidLoginError(OAuthError):

    def __init__(self, title='Invalid Login', **kwargs):
        super(InvalidLoginError, self).__init__(**kwargs)
        self.title = title
