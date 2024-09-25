import requests
import json
import uuid

# Authentication requests from https://github.com/TehFridge/Zappka3DS

class auth:
    """
    All functions used for authentication.
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
            
        return response.json()