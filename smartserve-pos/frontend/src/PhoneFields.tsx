import { useEffect, useId, useState } from "react";
import type { CountryCode } from "libphonenumber-js/max";
import { apiRequest } from "./api";

type PhoneCountry = { code: string; dial_code: string };
type PhoneFieldsProps = {
  country: string;
  phone: string;
  onCountryChange: (country: string) => void;
  onPhoneChange: (phone: string) => void;
  validationError: string;
};

const names = new Intl.DisplayNames(["en"], { type: "region" });
function phoneCountryName(code: string) {
  if (code === "KR") return "South Korea";
  if (code === "KP") return "North Korea";
  return names.of(code) ?? code;
}

type PhoneValidator = typeof import("libphonenumber-js/max");
function phoneValidationError(phone: string, country: string, validator: PhoneValidator) {
  const { isSupportedCountry, parsePhoneNumberFromString, validatePhoneNumberLength } = validator;
  const value = phone.trim();
  if (!value) return "";
  if (!isSupportedCountry(country)) return "Select a phone country.";
  const region = country as CountryCode;
  const countryName = phoneCountryName(region);
  const options = { defaultCountry: region, extract: false } as const;
  const parsed = parsePhoneNumberFromString(value, options);
  if (parsed?.country && parsed.country !== region) return `Enter a number for ${countryName}.`;
  const lengthError = validatePhoneNumberLength(value, options);
  if (lengthError === "TOO_SHORT") return `Number is too short for ${countryName}.`;
  if (lengthError === "TOO_LONG") return `Number is too long for ${countryName}.`;
  return parsed?.isValid() && parsed.country === region ? "" : `Enter a valid phone number for ${countryName}.`;
}

let validatorRequest: Promise<PhoneValidator> | undefined;
export function usePhoneValidation(phone: string, country: string) {
  const [validator, setValidator] = useState<PhoneValidator>();
  const [unavailable, setUnavailable] = useState(false);
  const shouldValidate = Boolean(phone.trim() && country);
  useEffect(() => {
    if (!shouldValidate || validator) return;
    let active = true;
    setUnavailable(false);
    validatorRequest ??= import("libphonenumber-js/max").catch(error => { validatorRequest = undefined; throw error; });
    validatorRequest.then(result => { if (active) setValidator(result); })
      .catch(() => { if (active) setUnavailable(true); });
    return () => { active = false; };
  }, [shouldValidate, validator]);
  if (!phone.trim()) return "";
  if (!country) return "Select a phone country.";
  if (!validator) return unavailable ? "Phone validation unavailable. Reload and try again." : "Checking phone number…";
  return phoneValidationError(phone, country, validator);
}

let countryRequest: Promise<PhoneCountry[]> | undefined;

function loadPhoneCountries() {
  countryRequest ??= apiRequest<PhoneCountry[]>("/business/phone-countries")
    .then(countries => countries.sort((a, b) => phoneCountryName(a.code).localeCompare(phoneCountryName(b.code))))
    .catch(error => { countryRequest = undefined; throw error; });
  return countryRequest;
}

export function PhoneFields({ country, phone, onCountryChange, onPhoneChange, validationError }: PhoneFieldsProps) {
  const phoneMessageId = useId();
  const [countries, setCountries] = useState<PhoneCountry[]>([]);
  const [error, setError] = useState(false);
  const [attempt, setAttempt] = useState(0);
  useEffect(() => {
    let active = true;
    loadPhoneCountries().then(list => { if (active) setCountries(list); })
      .catch(() => { if (active) setError(true); });
    return () => { active = false; };
  }, [attempt]);
  return <div className="phone-fields">
    <label>Phone country
      <select autoComplete="country" value={country} required={Boolean(phone.trim())} disabled={!countries.length} onChange={event => onCountryChange(event.target.value)}>
        <option value="">{countries.length ? "Choose country or territory" : error ? "Country list unavailable" : "Loading countries…"}</option>
        {countries.map(item => <option value={item.code} key={item.code}>{phoneCountryName(item.code)} ({item.dial_code})</option>)}
      </select>
    </label>
    {error && <button type="button" onClick={() => { setError(false); setAttempt(value => value + 1); }}>Retry loading countries</button>}
    <label>Phone (optional)
      <input type="tel" inputMode="tel" autoComplete="tel" maxLength={40}
        aria-invalid={Boolean(validationError)} aria-describedby={phoneMessageId}
        value={phone} onChange={event => onPhoneChange(event.target.value.replace(/[^0-9+(). -]/g, "").replace(/(?!^)\+/g, ""))} />
      <small id={phoneMessageId} className={validationError ? "phone-error" : undefined} aria-live="polite">
        {validationError || "Use a local number or include the selected country’s dialing code."}
      </small>
    </label>
  </div>;
}
