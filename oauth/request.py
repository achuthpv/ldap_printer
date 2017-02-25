from .exceptions import OAuthError
import requests
from credentials import API_URL


class RequestType(object):
    GET = 'get'
    POST = 'post'


class OAuthObject(object):
    def __init__(self, attr_dict):
        for key, val in attr_dict.items():
            if isinstance(val, (list, tuple)):
                setattr(self, key, [OAuthObject(x) if isinstance(x, dict) else x for x in val])
            else:
                setattr(self, key, OAuthObject(val) if isinstance(val, dict) else val)


class APIRequest(object):
    def __init__(self, url=None, method=RequestType.GET, access_token=None):
        self.kwargs = {
            'method': method,
            'url': url,
            'headers': {
                'Authorization': 'Bearer %s' % access_token
            },
        }
        self.response = None

    def _process_response(self):
        return self.response


class UserFieldAPIRequest(APIRequest):
    field_list = [
        'id',
        'username',
        'roll_number',
        'type',
        'is_alumni',
    ]

    def __init__(self, fields=None, **kwargs):
        url = kwargs.pop('url', API_URL)
        super(UserFieldAPIRequest, self).__init__(url=url, **kwargs)

        self.fields = []
        if fields and isinstance(fields, (list, tuple, set)):
            for field in fields:
                if field not in self.field_list:
                    raise OAuthError(message='Field %(field)s is not a valid field' % {'field': field})
                self.fields.append(field)
        else:
            self.fields = self.field_list

        self.oauth_user = None

    def get_oauth_user(self, refresh=False):
        if not self.oauth_user or refresh:
            self.oauth_user = None
            self._fetch_oauth_user()
        return self.oauth_user

    def _fetch_oauth_user(self):
        fields_val = ','.join(self.fields)
        query_params = {
            'fields': fields_val
        }
        self.kwargs['params'] = query_params
        response = requests.request(verify = False, **self.kwargs)
        if response.ok:
            try:
                json_response = response.json()
                self.oauth_user = OAuthObject(json_response)
            except ValueError:
                OAuthError(message='Unable to parse JSON', response=response)
        else:
            raise OAuthError(message='Got error while fetching user api response', response=response)
