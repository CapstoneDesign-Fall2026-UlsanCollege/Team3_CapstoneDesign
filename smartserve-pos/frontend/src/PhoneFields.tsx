import { useEffect, useState } from "react";
import { apiRequest } from "./api";

type PhoneCountry = { code: string; dial_code: string };
type PhoneFieldsProps = {
  country: string;
  phone: string;
  onCountryChange: (country: string) => void;
  onPhoneChange: (phone: string) => void;
};

const names = new Intl.DisplayNames(["en"], { type: "region" });
let countryRequest: Promise<PhoneCountry[]> | undefined;

function loadPhoneCountries() {
  countryRequest ??= apiRequest<PhoneCountry[]>("/business/phone-countries")
    .then(countries => countries.sort((a, b) => (names.of(a.code) ?? a.code).localeCompare(names.of(b.code) ?? b.code)))
    .catch(error => { countryRequest = undefined; throw error; });
  return countryRequest;
}

export function PhoneFields({ country, phone, onCountryChange, onPhoneChange }: PhoneFieldsProps) {
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
        {countries.map(item => <option value={item.code} key={item.code}>{names.of(item.code) ?? item.code} ({item.dial_code})</option>)}
      </select>
    </label>
    {error && <button type="button" onClick={() => { setError(false); setAttempt(value => value + 1); }}>Retry loading countries</button>}
    <label>Phone (optional)
      <input type="tel" inputMode="tel" autoComplete="tel" maxLength={40} value={phone} onChange={event => onPhoneChange(event.target.value)} />
      <small>Use a local number or include the selected country’s dialing code.</small>
    </label>
  </div>;
}
