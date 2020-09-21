import requests
import json
from requests.auth import AuthBase
from requests_toolbelt.multipart import encoder


class BearerAuth(AuthBase):
    def __init__(self, username):
        self.username = username
    
    def __call__(self, r):
        r.headers['Authorization'] = 'Bearer {}'.format(self.username)
        return r

if __name__ == '__main__':
    """
    url = 'http://127.0.0.1:8080/api/v1/npdb/01029663620'
    access_token = 'uxrFbQmFIodHZMHWcj3m5YFac9Yc9wzERmrQI1eonYokr7AtVeoRVVuGOpPl'

    response = requests.get(url, auth=BearerAuth(access_token))
    print(response.content)
    """ 
    """
    url = 'http://127.0.0.1:8080/api/mms'
    access_token = 'uxrFbQmFIodHZMHWcj3m5YFac9Yc9wzERmrQI1eonYokr7AtVeoRVVuGOpPl'
    files = [
        ('json', 'application/json', )
        ('images', ('lanncome.jpg', open('lanncome.jpg', 'rb'), 'image/jpg'))
        ]

    r = requests.post(url, auth=BearerAuth(access_token), files=files)
    print(r.text)
    """
    url = 'http://127.0.0.1:8080/api/mms'
    access_token = 'uxrFbQmFIodHZMHWcj3m5YFac9Yc9wzERmrQI1eonYokr7AtVeoRVVuGOpPl'
    payload = {"key": "1", "phone": "01029663620", "callback": "1004", "msg": "test message"}
    multipart_encoder = encoder.MultipartEncoder(
        fields={
            #'json': (None, json.dumps(payload), 'application/json')
            'image': ('lanncome.jpg', open('lanncome.jpg', 'rb'), 'image/jpg'),
            'json': ('1.json', json.dumps(payload), 'application/json')
        }
    )
    headers = {
        'Content-Type': multipart_encoder.content_type
    }
    r = requests.post(url, auth=BearerAuth(access_token), data=multipart_encoder, headers=headers)