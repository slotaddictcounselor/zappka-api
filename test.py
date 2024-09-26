import zappka

# Get token needed for phone authorization
temp_auth_token = zappka.auth.get_temp_auth_token()

# Get info from user
apiKey = input("API key: ")
phone_number = input("Enter phone number (ex. 123456789): ")
country_code = input("Enter country code (ex. 48): ")

print("Sending SMS authentication request.")

# Send phone authorization request. Sends a message to given phone number.
zappka.auth.phone_auth_init(temp_auth_token, country_code, phone_number)

print(f"+{country_code}{phone_number} should receive a message with a verification code.")

# Get code from user
sms_code = input("Enter received SMS code: ")

auth_token = zappka.auth.phone_auth(temp_auth_token, country_code, phone_number, sms_code)

if auth_token == False:
    print("Something went wrong during authentication (no token in response)")
    exit()
else:
    print(f"Successfully authenticated!")

print("Verifying custom token.")

identityProviderToken = zappka.auth.verify_custom_token(auth_token)

if identityProviderToken == False:
    print("Something went wrong during verification (idToken missing)")
    exit()
else:
    print("Custom token verified.")

# Required so the API won't cry about not starting a session or something.
zappka.auth.get_account_info(identityProviderToken)



