"""Country-aware business phone validation using libphonenumber metadata."""
import re

from fastapi import HTTPException
import phonenumbers

PHONE_COUNTRIES = [
    {"code": code, "dial_code": f"+{phonenumbers.country_code_for_region(code)}"}
    for code in sorted(phonenumbers.SUPPORTED_REGIONS)
]


def normalize_phone(value: str, country: str) -> str:
    value = value.strip()
    if not value:
        return ""
    country = country.strip().upper()
    if country not in phonenumbers.SUPPORTED_REGIONS:
        raise HTTPException(422, "Choose the country or territory for this phone number.")
    error = "Enter a valid phone number for the selected country. Check its country code and length."
    if not re.fullmatch(r"\+?[0-9().\- \t]+", value):
        raise HTTPException(422, error)
    try:
        number = phonenumbers.parse(value, country)
    except phonenumbers.NumberParseException:
        raise HTTPException(422, error) from None
    if not phonenumbers.is_valid_number_for_region(number, country):
        raise HTTPException(422, error)
    return phonenumbers.format_number(number, phonenumbers.PhoneNumberFormat.E164)


def phone_country(value: str) -> str:
    if not value or not value.startswith("+"):
        return ""
    try:
        number = phonenumbers.parse(value, None)
    except phonenumbers.NumberParseException:
        return ""
    region = phonenumbers.region_code_for_number(number)
    return region if region and phonenumbers.is_valid_number_for_region(number, region) else ""
