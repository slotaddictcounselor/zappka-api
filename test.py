import zappka

# Get token needed for phone authorization
temp_auth_token = zappka.auth.get_temp_auth_token()

phone_number = input("Enter phone number (ex. 123456789): ")
country_code = input("Enter country code (ex. 48): ")

print("Sending SMS authentication request.")

# Send phone authorization request. Sends a message to given phone number.
zappka.auth.phone_auth_init(temp_auth_token, country_code, phone_number)

print(f"+{country_code}{phone_number} should receive a message with a verification code.")

sms_code = input("Enter received SMS code: ")

token = zappka.auth.phone_auth(temp_auth_token, country_code, phone_number, sms_code)

if token == False:
    print("Something went wrong during authentication (no token in response)")
    exit()
else:
    print(f"Successfully authenticated!")

print("Verifying custom token.")

identityProviderToken = zappka.auth.verify_custom_token(token)

if identityProviderToken == False:
    print("Something went wrong during verification (idToken or refreshToken missing)")
    exit()
else:
    print("Custom token verified.")

zappka.auth.get_account_info(identityProviderToken)

print(zappka.account.get_details(identityProviderToken))