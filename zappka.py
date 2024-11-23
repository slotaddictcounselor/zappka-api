import requests
import json

class auth:
    def send_verification_code(number, country):
        try:
            idToken = requests.post(
                "https://www.googleapis.com/identitytoolkit/v3/relyingparty/signupNewUser?key=AIzaSyDe2Fgxn_8HJ6NrtJtp69YqXwocutAoa9Q",
                headers = {
                    "content-type": "application/json"
                },
                data = json.dumps({
                        "clienttype": "CLIENT_TYPE_ANDROID"
                })
            ).json()['idToken']
            
            req = requests.post(
                "https://super-account.spapp.zabka.pl",
                headers = {
                    "content-type": "application/json",
                    "authorization": "Bearer " + idToken
                },
                data = json.dumps({
                    "operationName": "SendVerificationCode",
                    "query": "mutation SendVerificationCode($input: SendVerificationCodeInput!) { sendVerificationCode(input: $input) { retryAfterSeconds } }",
                    "variables": {
                        "input": {
                            "phoneNumber": {
                                "countryCode": country,
                                "nationalNumber": number,
                            }
                        }
                    }
                })
            )
            
            return idToken
        except Exception:
            return [False, Exception]
        
    def sms_auth(number, country, sms, idToken):
        try:
            req = requests.post(
                "https://super-account.spapp.zabka.pl/",
                headers = {
                    "content-type": "application/json",
                    "authorization": "Bearer " + idToken,
                    "user-agent": "okhttp/4.12.0",
                    "x-apollo-operation-id": "a531998ec966db0951239efb91519560346cfecac77459fe3b85c5b786fa41de",
                    "x-apollo-operation-name": "SignInWithPhone",
                    "accept": "multipart/mixed; deferSpec=20220824, application/json",
                },
                data = json.dumps({
                    "operationName": "SignInWithPhone",
                    "variables": {
                        "input": {
                            "phoneNumber": {
                                "countryCode": country, 
                                "nationalNumber": number,
                            },
                            "verificationCode": sms,
                        }
                    },
                    "query": "mutation SignInWithPhone($input: SignInInput!) { signIn(input: $input) { customToken } }"
                })
            )
            
            customToken = req.json()['data']['signIn']['customToken']
            
            req2 = requests.post(
                "https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyCustomToken?key=AIzaSyDe2Fgxn_8HJ6NrtJtp69YqXwocutAoa9Q",
                headers = {
                    "content-type": "application/json",
                },
                data = json.dumps({
                    "token": customToken,
                    "returnSecureToken": "True",
                })
            )
            
            return req2.json()['idToken']
        except Exception:
            return [False, Exception]
        
class spapp:
    class api:
        def check_soft_ban(secureToken, ua):
            req = requests.post(
                "https://api.spapp.zabka.pl/",
                headers = {
                    "user-agent": ua,
                    "accept": "application/json",
                    "content-type": "application/json",
                    "authorization": "Bearer " + secureToken
                },
                data = json.dumps({
                    "operationName": "CheckSoftBan",
                    "query": "query CheckSoftBan { userProfileStatus { banStatus { isSoftBanned } } }",
                    "variables": {}
                })
            )
            
            return req.json()['data']['userProfileStatus']['banStatus']['isSoftBanned']
        
        def get_available_zappsy(secureToken, ua):
            req = requests.post(
                "https://api.spapp.zabka.pl/",
                headers = {
                    "user-agent": ua,
                    "accept": "application/json",
                    "content-type": "application/json",
                    "authorization": "Bearer " + secureToken
                },
                data = json.dumps({
                    "operationName": "LoyaltyPoints",
                    "query": "query LoyaltyPoints { loyaltyProgram { points pointsStatus pointsOperationsAvailable } }",
                    "variables": {}
                })
            )
            
            return req.json()['data']['loyaltyProgram']['points']