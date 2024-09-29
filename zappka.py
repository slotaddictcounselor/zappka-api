import requests
import json
import uuid

# Authentication requests from https://github.com/TehFridge/Zappka3DS

class auth:

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
        Returns identityProviderToken. Used for zabka-snrs token and Superlogin requests.
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

        return response.json()
        
class superlogin:

    def get_details(token):
        """
        Requires secure token (verify_custom_token). Returns account information.
        (first name, birth date, phone number and e-mail)
        """
        url = "https://super-account.spapp.zabka.pl/"

        headers = {
            "authorization": "Bearer " + token,
            "content-type": "application/json",
            "sec-fetch-site": "cross-site",
            "sec-fetch-mode": "cors",
            "sec-fetch-dest": "empty",
            "sec-ch-ua-platform": "Android",
            "sec-ch-ua-mobile": "71",
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7",
            "dnt": "1",
            "origin": "https://czs.superlogin.pl",
            "referer": "https://czs.superlogin.pl/",
        }

        data = {
            "operationName": "Profile",
            "query": "\n  query Profile {\n    profile {\n      id\n      firstName\n      birthDate\n      phoneNumber {\n        countryCode\n        nationalNumber\n      }\n      deleteRequestedAt\n      email\n    }\n  }\n"
        }

        response = requests.post(url, headers=headers, data=json.dumps(data))

        return response.json()

    def change_details(token, variable, value):
        """
        Requires secure token (verify_custom_token).
        Changes account details:
            "birthDate": "YYYY-MM-DD"
            "firstName": "name"
            "email": "email@example.com"
        """
        url = "https://super-account.spapp.zabka.pl/"

        headers = {
            "authorization": "Bearer " + token,
            "content-type": "application/json",
            "sec-fetch-site": "cross-site",
            "sec-fetch-mode": "cors",
            "sec-fetch-dest": "empty",
            "sec-ch-ua-platform": "Android",
            "sec-ch-ua-mobile": "71",
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7",
            "dnt": "1",
            "origin": "https://czs.superlogin.pl",
            "referer": "https://czs.superlogin.pl/",
        }

        data = {
            "query": "\n    mutation UpdateProfile($input: UpdateProfileInput!) {\n  updateProfile(input: $input) {\n    id\n  }\n}\n    ",
            "variables": {
                "input": {
                    variable: value,
                }
            }
        }

        response = requests.post(url, headers=headers, data=json.dumps(data))
        
        return response.json()

class snrs:

    def get_snrs_token(token, apiKey):
        """
        Requires identityProviderToken.
        """
        uid = str(uuid.uuid4())

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

    def get_zappsy_amount(token):
        """
        Requires snrs token. Returns żappsy amount.
        """
        url = "https://zabka-snrs.zabka.pl/schema-service/v2/documents/points/generate"

        headers = {
            "Cache-Control": "no-cache", 
            "api-version": "4.4", 
            "application-id": "%C5%BCappka", 
            "user-agent": "Synerise Android SDK 5.9.0 pl.zabka.apb2c", 
            "accept": "application/json", 
            "mobile-info": "horizon;28;AW700000000;9;CTR-001;nintendo;5.9.0", 
            "content-type": "application/json; charset=UTF-8", 
            "authorization": token
        }

        response = requests.get(url, headers=headers)

        return response.json()['content']['points']

    def transfer_zappsy(token, phoneNumber, amount, message):
        """
        Requires snrs token and phone number of the user you want to send żappsy to.
        """

        # request 1 - get client id from phone number

        url = f"https://api.zappka.app/transfer-points/users/phone-number/{phoneNumber}"

        headers = {
           "Authorization": token,
           "Content-Type": "application/json",
           "API-Version": "12",
           "App-Version": "3.21.60",
           "App-Platform": "android",
           "App-Device": "samsung SM-A600FN",
           "Accept-Encoding": "gzip",
           "User-Agent": "okhttp/4.12.0"
        }
        
        response = requests.get(url, headers=headers)
        clientId = response.json()["client_id"]

        # request 2 - transfer żappsy to another account

        url = f"https://api.zappka.app/transfer-points/users/{clientId}"

        # reusing headers from previous request

        data = {
            "sender_name": "S", # to do: get sender_name from superlogin account details
            "recipient_name": "R", # and maybe figure out how to get recipient name
            "points_number": amount,
            "message": message,
        }

        response = requests.post(url, headers=headers, data=json.dumps(data))
        
        return response.json()['status']