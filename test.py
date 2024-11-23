import zappka
import uuid

number = input("[?] Input phone number (ex. 500123789): ")
country = input("[?] Input country code (ex. 48): ")

idToken = zappka.auth.send_verification_code(number, country)

print("[.] SMS code sent.")
    
sms = input("[?] Enter received SMS code (XXXXXX): ")

secureToken = zappka.auth.sms_auth(number, country, sms, idToken)

uuid0 = uuid.uuid4()
print(f"[.] Random UUID: {uuid0}")

ua = f"Zappka/40038 (py; x/x; {uuid0}) REL/28"

softbanned = zappka.spapp.api.check_soft_ban(secureToken, ua)
print(f"[.] Softbanned?: {softbanned}")

available_zappsy = zappka.spapp.api.get_available_zappsy(secureToken, ua)
print(f"[.] Available żappsy: {available_zappsy}")