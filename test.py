import superlogin

temp_auth_token = superlogin.get_temp_auth_token()

phone_number = input("Enter phone number (ex. 123456789): ")
country_code = input("Enter country code (ex. 48): ")

print("Sending SMS authentication request.")

print(superlogin.phone_auth_init(temp_auth_token, country_code, phone_number))

print(f"+{country_code}{phone_number} should receive a message with a verification code.")

sms_code = input("Enter received SMS code: ")

print(superlogin.phone_auth(temp_auth_token, country_code, phone_number, sms_code))