import requests
import json
import uuid

# Authentication requests from https://github.com/TehFridge/Zappka3DS

class auth:
    """
    Functions related to authentication.
    """

    def get_temp_auth_token():
        """
        Used for phone authentication.
        """
        url = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/signupNewUser?key=AIzaSyDe2Fgxn_8HJ6NrtJtp69YqXwocutAoa9Q"
        
        headers = {
            "content-type": "application/json"
        }

        data = {
            "clientType": "CLIENT_TYPE_ANDROID"
        }

        response = requests.post(url, headers=headers, data=json.dumps(data))
            
        return response.json()['idToken']

    def phone_auth_init(temp_auth_token, country_code, phone_number):
        """
        Start phone number authentication.
        Request sends SMS message to given phone number.
        """
        url = "https://super-account.spapp.zabka.pl/"

        headers = {
            "content-type": "application/json",
            "authorization": "Bearer " + temp_auth_token,
        }

        data = {
            "operationName": "SendVerificationCode",
            "query": "mutation SendVerificationCode($input: SendVerificationCodeInput!) { sendVerificationCode(input: $input) { retryAfterSeconds } }",
            "variables": {
                "input": {
                    "phoneNumber": {
                        "countryCode": country_code,
                        "nationalNumber": phone_number,
                    }
                }
            }
        }

        response = requests.post(url, headers=headers, data=json.dumps(data))
            
        return response.json()


    def phone_auth(temp_auth_token, country_code, phone_number, verify_code):
        """
        Complete phone number authentication.
        Sends the code from SMS message to Żabka.
        Returns token.

        Uses token from get_temp_auth_token()
        """
        url = "https://super-account.spapp.zabka.pl/"

        headers = {
            "content-type": "application/json",
            "authorization": "Bearer " + temp_auth_token,
            "user-agent": "okhttp/4.12.0",
            "x-apollo-operation-id": "a531998ec966db0951239efb91519560346cfecac77459fe3b85c5b786fa41de",
            "x-apollo-operation-name": "SignInWithPhone",
            "accept": "multipart/mixed; deferSpec=20220824, application/json",
            "content-length": "250",
        }

        data = {
            "operationName": "SignInWithPhone",
            "variables": {
                "input": {
                    "phoneNumber": {
                        "countryCode": country_code, 
                        "nationalNumber": phone_number,
                    },
                    "verificationCode": verify_code,
                }
            },
            "query": "mutation SignInWithPhone($input: SignInInput!) { signIn(input: $input) { customToken } }"
        }

        response = requests.post(url, headers=headers, data=json.dumps(data))
            
        if response.json()['data']['signIn']['customToken']:
            return response.json()['data']['signIn']['customToken']
        else:
            return False
        
    def verify_custom_token(token):
        """
        Requires token received after phone authentication.
        Returns yet another token and refreshToken.
        """
        url = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyCustomToken?key=AIzaSyDe2Fgxn_8HJ6NrtJtp69YqXwocutAoa9Q"

        headers = {
            "content-type": "application/json",
        }

        data = {
            "token": token,
            "returnSecureToken": "True",
        }

        response = requests.post(url, headers=headers, data=json.dumps(data))

        if response.json()['idToken']:
            return response.json()['idToken']
        else:
            return False
        
    def get_account_info(token):
        url = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/getAccountInfo?key=AIzaSyDe2Fgxn_8HJ6NrtJtp69YqXwocutAoa9Q"

        headers = {
            "content-type": "application/json"
        }

        data = {
            "idToken": token,
        }

        response = requests.post(url, headers=headers, data=json.dumps(data))
        print(response.json())

        return response.json()
        
    def get_main_token(token):
        uid = str(uuid.uuid4())
        print(uid)
        apiKey = "00000000-0000-0000-0000-000000000000" # Not provided.

        url = "https://zabka-snrs.zabka.pl/sauth/v3/auth/login/client/conditional"

        headers = {
            "api-version": "4.4",
            "application-id": "%C5%BCappka",
            "user-agent": "Synerise Android SDK 5.9.0 pl.zabka.apb2c",
            "accept": "application/json",
            "content-type": "application/json; charset=UTF-8",
            "mobile-info": "horizon;28;AW700000000;9;CTR-001;nintendo;5.9.0",
        }

        data = {
            "identityProviderToken": token,
            "identityProvider": "OAUTH",
            "apiKey": apiKey,
            "uuid": uid,
            "deviceId": "0432b18513e325a5",
        }

        response = requests.post(url, headers=headers, data=json.dumps(data))
        
        if response.json()['token']:
            return response.json()['token']
        else:
            return False