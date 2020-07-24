import requests
import json
from requests.auth import HTTPBasicAuth
from datetime import datetime
import base64

class MpesaC2bCredentials:
    consumer_key='jAwDSq2OYYhDdUBmUBcePcO1uXwS43Vb'
    consumer_secret='Pfe0j4cMYI9W4WIS'
    api_url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'


def MpesaAccessToken(request):
    r = requests.get(MpesaC2bCredentials.api_url,
                        auth=HTTPBasicAuth(MpesaC2bCredentials.consumer_key, 
                        MpesaC2bCredentials.consumer_secret))
    
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token['access_token']


    return str(validated_mpesa_access_token)


class MpesaPassword:
    lipa_time = datetime.now().strftime('%Y%m%d%H%M%S')
    Business_short_code = "174379"
    passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
    data_to_encode = Business_short_code + passkey + lipa_time
    online_password = base64.b64encode(data_to_encode.encode())
    decode_password = online_password.decode('utf-8')
    