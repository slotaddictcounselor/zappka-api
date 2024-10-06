# Żappka & Superlogin API

- [Żappka \& Superlogin API](#żappka--superlogin-api)
  - [Współautorzy](#współautorzy)
  - [Przykłady](#przykłady)
    - [Logowanie](#logowanie)
    - [Żądania API Synerise](#żądania-api-synerise)
    - [Żądania API Superlogin](#żądania-api-superlogin)
    - [Kod QR](#kod-qr)
  - [Info](#info)

## Współautorzy

[TehFridge](https://github.com/tehfridge) - logowanie się i żądania API Synerise

[domints](https://github.com/domints) - obliczanie TOTP do kodów QR

## Przykłady

### Logowanie

Poniższy skrypt pokazuje jak można zalogować się numerem telefonu.

```python
import zappka

numer_telefonu = input("Podaj swój numer telefonu: ")
numer_kierunkowy = input("Podaj numer kierunkowy kraju (np. 48): ")

idToken = zappka.auth.get_idToken()
zappka.auth.phone_auth_init(idToken, numer_kierunkowy, numer_telefonu)

kod_sms = input("Wpisz kod otrzymany wiadomością SMS: ")

customToken = zappka.auth.phone_auth(idToken, numer_kierunkowy, numer_telefonu, kod_sms)
identityProviderToken = zappka.auth.verify_custom_token(customToken)
```

`identityProviderToken` jest używany do żądań API Superloginu oraz do kodów QR.

Tym tokenem można również zdobyć `snrsToken`, który jest potrzebny do żądań API Synerise.

### Żądania API Synerise

Po zalogowaniu się numerem telefonu, możesz użyć `identityProviderToken` aby zdobyć `snrsToken`.

```python
# Tutaj logowanie numerem telefonu

snrsToken = zappka.snrs.get_snrs_token(identityProviderToken)
```

Teraz za pomocą tego tokenu możesz:

- zdobyć ilość Żappsów (dostępne i łącznie zdobyte)

```python
dostepne = zappka.snrs.get_current_ilosc_zappsow(snrsToken)
lacznie_zdobyte = zappka.snrs.get_alltime_ilosc_zappsow(snrsToken)
```

- zdobyć informacje o twoim koncie Żappka (m.in. numer telefonu, email czy nawet ID konta Discord połączonego z kontem Żappka)

```python
zappka.snrs.get_personal_information(snrsToken)
```

- przelewać Żappsy na inne konto poprzez numer telefonu

```python
numer_odbiorcy = input("Wpisz numer telefonu odbiorcy: ")

ilosc_zappsow = int(input("Ile Żappsów chcesz wysłać?: ")
# Ilość wysyłanych Żappsów musi być podana jako liczba całkowita.

wiadomosc = input("Wpisz wiadomość: ")
# Wiadomość dołączona z przelewem.

imie = zappka.snrs.get_personal_information(snrsToken)['imie']
# Z jakiegoś powodu można w przelewach dać dowolny tekst.

zappka.snrs.transfer_zappsy(snrsToken, numer_odbiorcy, ilosc_zappsow, wiadomosc, imie)
```

- zdobyć historię Żappsów (zdobyte ze sklepów, wysłane do innych, itp.)

```python
zappka.snrs.get_zappsy_history(snrsToken)
# Notka: w niektórych przypadkach może zwrócić bardzo długą listę
```

- odbierać kupony (wkrótce)

### Żądania API Superlogin

Superlogin służy do zarządzania kontem Żappka. Pozwala na zmianę imienia, maila oraz daty urodzenia ~~(również numeru telefonu ale nie jest to jeszcze zaimplementowane)~~.

Z racji tego, że Superlogin używa tego samego endpointu do zmieniania wszystkich danych, połączyłem je w jedną funkcję.

```python
# Zmień imię
zappka.superlogin.change_details(identityProviderToken, "firstName", "Maciek")

# Zmień maila
zappka.superlogin.change_details(identityProviderToken, "email", "twojemail@example.com")

# Zmień datę urodzenia
zappka.superlogin.change_details(identityProviderToken, "birthDate", "2000-04-30")

```

### Kod QR

Kody QR są bardziej skomplikowane niż po prostu wysyłanie żądania i branie danych z odpowiedzi.

Aby mieć poprawny kod QR należy:

- zdobyć userId i sekret z `https://qr-bff.spapp.zabka.pl/qr-code/secret`
- obliczyć TOTP z sekretu
- użyć userId i TOTP aby stworzyć link zlgn.pl (np: `https://zlgn.pl/view/dashboard?ploy=0&loyal=123456`)
  - te linki zawsze zwracają 404
- link zlgn.pl jest później wyświetlany jako kod QR

Poniżej jest przykładowy skrypt pokazujący jak zdobyć link i wyświetlić go w terminalu jako kod QR.

```python
import zappka
import qrcode # pip install qrcode

# Tutaj logowanie numerem telefonu

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

Ten projekt nie jest w żaden sposób powiązany z Żabka Group S.A. API oraz znaki towarowe są własnością Żabka Group.
