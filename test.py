# This script has no error handlers or anything like that. Purely for testing purposes.
# Overall this script is a mess.
import zappka
import qrcode # Print QR code to console

# Get token needed for phone authorization
temp_auth_token = zappka.auth.get_temp_auth_token()

# Get info from user
phone_number = input("Enter phone number (ex. 123456789): ")
country_code = input("Enter country code (ex. 48): ")

print("Sending SMS authentication request.")

# Send phone authorization request. Sends a message to given phone number.
zappka.auth.phone_auth_init(temp_auth_token, country_code, phone_number)

print("You should receive a message with a verification code.")

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

apiKey = input("API key: ")

snrs_token = zappka.snrs.get_snrs_token(identityProviderToken, apiKey)

while True:
    print("\n")
    print("Main")
    print("1. Superlogin")
    print("2. Synerise")
    print("3. QR")
    print("4. Exit")
    choice = int(input("> "))

    match choice:
        case 1:
            while True:
                print("\n")
                print("Main > Superlogin")
                print("1. Change first name.")
                print("2. Change email.")
                print("3. Change birth date (YYYY-MM-DD).")
                print("4. Get account details")
                print("5. Exit.")

                choice = int(input("> "))

                match choice:
                    case 1:
                        try:
                            value = input("Enter name: ")
                            zappka.superlogin.change_details(identityProviderToken, "firstName", value)
                        except KeyboardInterrupt:
                            pass
                    case 2:
                        try:
                            value = input("Enter email: ")
                            zappka.superlogin.change_details(identityProviderToken, "email", value)
                        except KeyboardInterrupt:
                            pass
                    case 3:
                        try:
                            value = input("Enter birth date (YYYY-MM-DD): ")
                            zappka.superlogin.change_details(identityProviderToken, "birthDate", value)
                        except KeyboardInterrupt:
                            pass
                    case 4:
                        print(zappka.superlogin.get_details(identityProviderToken))
                    case 5:
                        break
                    case _:
                        print("?")
        case 2:
            while True:
                print("\n")
                print("Main > Synerise")
                print("1. Get żappsy amount")
                print("2. Transfer żappsy")
                print("3. Get personal information")
                print("4. Exit")

                choice = int(input("> "))

                match choice:
                    case 1:
                        print(zappka.snrs.get_zappsy_amount(snrs_token))
                    case 2:
                        try:
                            phoneNumber = input("Enter recipient phone number (ex. 123456789): ")
                            amount = int(input("Enter amount of żappsy: "))
                            message = input("Enter message: ")
                            anonymous = input("Anonymous (replace first name)? [Y/N/C, default: N]: ")
                            match anonymous:
                                case "Y":
                                    anonymous = True
                                case "N":
                                    anonymous = False
                                case "C":
                                    break
                                case _:
                                    anonymous = False

                            if zappka.snrs.transfer_zappsy(snrs_token, phoneNumber, amount, message, anonymous) == "PROCESSING":
                                print(f"Successfully sent {amount} żappsy.")
                            else:
                                pass
                        except KeyboardInterrupt:
                            pass
                    case 3:
                        print(zappka.snrs.get_personal_information(snrs_token))
                    case 4:
                        break
                    case _:
                        print("?")
        case 3:
            while True:
                print("1. Show QR code")
                print("2. Exit")

                choice = int(input("> "))

                match choice:
                    case 1:
                        url = zappka.qr.get_qr_code(identityProviderToken)

                        # Show URL as QR code
                        qr = qrcode.QRCode(
                                version=1,
                                error_correction=qrcode.constants.ERROR_CORRECT_L,
                                box_size=10,
                                border=4,
                        )
                        qr.add_data(url)
                        qr.print_ascii(invert=True)

                        print(url)
                    case 2:
                        break
                    case _:
                        print("?")
        case 4:
            exit()