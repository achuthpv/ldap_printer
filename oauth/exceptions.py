class OAuthError(Exception):

    def __init__(self, message=None, response=None):
        super(OAuthError, self).__init__(message)
        self.response = response