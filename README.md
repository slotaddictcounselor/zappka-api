# Żappka & Superlogin API

- [Żappka \& Superlogin API](#żappka--superlogin-api)
  - [Installation](#installation)
  - [Credits](#credits)
  - [Examples](#examples)
    - [Authentication](#authentication)
    - [Synerise API requests](#synerise-api-requests)
    - [Superlogin API requests](#superlogin-api-requests)
    - [QR code](#qr-code)
  - [Info](#info)

## Installation

```bash
git clone https://github.com/slotaddictcounselor/zappka-api
cd ./zappka-api
pip install requests
```

`requests` is the only library used in `zappka.py` that is not available on a fresh Python install.

## Credits

[TehFridge](https://github.com/tehfridge) - Synerise API and authorization requests

[domints](https://github.com/domints) - TOTP implementation for QR codes

## Examples

### Authentication

The following script shows how you can authenticate using your phone number.

```python
import zappka

phone_number = input("Enter your phone number: ")
country_code = input("Enter your number's country code: ")

idToken = zappka.auth.get_idToken()
zappka.auth.phone_auth_init(idToken, country_code, phone_number)

sms_code = input("Enter received SMS code: ")

customToken = zappka.auth.phone_auth(idToken, country_code, phone_number, sms_code)
identityProviderToken = zappka.auth.verify_custom_token(customToken)
```

`identityProviderToken` can be used for interactions with the Superlogin or QR code API.

You can also get the token required for Synerise API requests.

### Synerise API requests

After phone authentication, you can use the identityProviderToken to get the token required for Synerise API requests.

```python
# Phone authentication

snrsToken = zappka.snrs.get_snrs_token(identityProviderToken)
```

Now using that token you can:

- get the amount of Żappsy (current and all-time)

```python
current = zappka.snrs.get_current_zappsy_amount(snrsToken)
alltime = zappka.snrs.get_alltime_zappsy_amount(snrsToken)
```

- get personal information

```python
zappka.snrs.get_personal_information(snrsToken)
```

- transfer Żappsy to a different account (phone number)

```python
recipient_number = input("Enter recipient's phone number: ")

zappsy_amount = int(input("How much żappsy do you want to send?: ")
# Amount needs to be integer.

message = input("Enter message: ")
# Message displayed in transfer, required.

firstName = zappka.snrs.get_personal_information(snrsToken)['firstName']
# You can also set any string as firstName

zappka.snrs.transfer_zappsy(snrsToken, recipient_number, zappsy_amount, message, firstName)
```

- get Żappsy history (received from stores, sent to people, etc.)

```python
zappka.snrs.get_zappsy_history(snrsToken)
# Note: might return extremely long list
```

- redeem coupons (soon)

### Superlogin API requests

Superlogin is an account management service created by Żabka. It allows you to change your first name, email and birth date ~~(also phone number but not in Python module)~~. As far as I know it's used only for Żappka.

Since Superlogin uses the same endpoint for all account details, I decided to combine them into one function.

```python
# Change first name
zappka.superlogin.change_details(identityProviderToken, "firstName", "Maciek")

# Change email
zappka.superlogin.change_details(identityProviderToken, "email", "iamnottheownerof@example.com")

# Change birth date
zappka.superlogin.change_details(identityProviderToken, "birthDate", "2000-04-30")

```

### QR code

QR codes are more complicated than just sending a request and taking data from response.

In order to get a valid QR code you need to:

- get userId and secret from `https://qr-bff.spapp.zabka.pl/qr-code/secret`
- calculate TOTP from secret
- use userID and TOTP to create a zlgn.pl URL (ex: `https://zlgn.pl/view/dashboard?ploy=0&loyal=123456`)
  - the URLs will always return 404 error code no matter what (unless they are supposed to be accessed only by Żabka QR code scanners or something idk)
- the zlgn.pl URL is then displayed as a QR code

Below is an example script that gets the zlgn.pl URL and prints it to terminal as a QR code.

```python
import zappka
import qrcode # pip install qrcode

# Phone authentication here

url = zappka.qr.get_qr_code(identityProviderToken)
# https://zlgn.pl/view/dashboard?ploy={userId}&loyal={totp}

qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)

qr.add_data(url)
qr.print_ascii(invert=True)
```

## Info

Not affiliated with or endorsed by Żabka Group S.A. API and trademarks are property of Żabka Group S.A.
