import superlogin

# Get token needed for phone authorization
temp_auth_token = superlogin.auth.get_temp_auth_token()

phone_number = input("Enter phone number (ex. 123456789): ")
country_code = input("Enter country code (ex. 48): ")

print("Sending SMS authentication request.")

# Send phone authorization request. Sends a message to given phone number.
superlogin.auth.phone_auth_init(temp_auth_token, country_code, phone_number)

print(f"+{country_code}{phone_number} should receive a message with a verification code.")

sms_code = input("Enter received SMS code: ")

token = superlogin.auth.phone_auth(temp_auth_token, country_code, phone_number, sms_code)

if token == False:
    print("Something went wrong during authentication (no token in response)")
    exit()
else:
    print(f"Successfully authenticated!")

print("Verifying custom token.")

custom_token = superlogin.auth.verify_custom_token(token)

if custom_token == False:
    print("Something went wrong during verification (idToken or refreshToken missing)")
    exit()
else:
    print("Custom token verified.")

print("Retrieving main token.")

superlogin.auth.get_account_info(custom_token)

main_token = superlogin.auth.get_main_token(custom_token)

if main_token == False:
    print("Something went wrong while retrieving the main token.")
else:
    print("Main token received.")