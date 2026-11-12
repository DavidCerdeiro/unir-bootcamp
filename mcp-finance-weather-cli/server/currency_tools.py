"""Herramientas de conversion de monedas (ExchangeRate-API)."""

import logging

from server.api_clients import ApiClientError, fetch_exchange_rates

logger = logging.getLogger(__name__)

# Monedas mostradas por defecto al pedir las tasas de una moneda base.
MONEDAS_HABITUALES = ["EUR", "USD", "GBP", "JPY", "CHF", "MXN", "ARS", "COP", "BRL", "CNY"]

# Set de validación de códigos ISO 4217
ISO_4217_CODES = {
    "AED", "AFN", "ALL", "AMD", "ANG", "AOA", "ARS", "AUD", "AWG", "AZN", "BAM", "BBD", "BDT", "BGN", "BHD", "BIF",
    "BMD", "BND", "BOB", "BRL", "BSD", "BTN", "BWP", "BYN", "BZD", "CAD", "CDF", "CHF", "CLP", "CNY", "COP", "CRC",
    "CUP", "CVE", "CZK", "DJF", "DKK", "DOP", "DZD", "EGP", "ERN", "ETB", "EUR", "FJD", "FKP", "FOK", "GBP", "GEL",
    "GGP", "GHS", "GIP", "GMD", "GNF", "GTQ", "GYD", "HKD", "HNL", "HRK", "HTG", "HUF", "IDR", "ILS", "IMP", "INR",
    "IQD", "IRR", "ISK", "JEP", "JMD", "JOD", "JPY", "KES", "KGS", "KHR", "KID", "KMF", "KRW", "KWD", "KYD", "KZT",
    "LAK", "LBP", "LKR", "LRD", "LSL", "LYD", "MAD", "MDL", "MGA", "MKD", "MMK", "MNT", "MOP", "MRU", "MUR", "MVR",
    "MWK", "MXN", "MYR", "MZN", "NAD", "NGN", "NIO", "NOK", "NPR", "NZD", "OMR", "PAB", "PEN", "PGK", "PHP", "PKR",
    "PLN", "PYG", "QAR", "RON", "RSD", "RUB", "RWF", "SAR", "SBD", "SCR", "SDG", "SEK", "SGD", "SHP", "SLE", "SLL",
    "SOS", "SRD", "SSP", "STN", "SYP", "SZL", "THB", "TJS", "TMT", "TND", "TOP", "TRY", "TTD", "TVD", "TWD", "TZS",
    "UAH", "UGX", "USD", "UYU", "UZS", "VES", "VND", "VUV", "WST", "XAF", "XCD", "XDR", "XOF", "XPF", "YER", "ZAR",
    "ZMW", "ZWL"
}

def convert_currency(amount: float, from_currency: str, to_currency: str) -> dict:
    """Convierte una cantidad entre dos divisas con la tasa de cambio actual.

    Args:
        amount: cantidad a convertir (mayor que 0).
        from_currency: codigo ISO 4217 de la moneda origen (p. ej. USD).
        to_currency: codigo ISO 4217 de la moneda destino (p. ej. EUR).
    """
    if amount <= 0:
        raise ValueError("La cantidad a convertir debe ser estrictamente mayor que 0.")
    
    if not isinstance(from_currency, str) or from_currency.strip().upper() not in ISO_4217_CODES:
        raise ValueError(f"La moneda origen '{from_currency}' debe ser un código ISO 4217 válido (ej. USD).")
    
    if not isinstance(to_currency, str) or to_currency.strip().upper() not in ISO_4217_CODES:
        raise ValueError(f"La moneda destino '{to_currency}' debe ser un código ISO 4217 válido (ej. EUR).")

    from_currency = from_currency.strip().upper()
    to_currency = to_currency.strip().upper()

    logger.info(f"Convirtiendo {amount} {from_currency} a {to_currency}")
    
    rates = fetch_exchange_rates(from_currency)
    
    if to_currency not in rates:
        raise ApiClientError(f"La moneda de destino '{to_currency}' no está disponible en las tasas obtenidas.")

    exchange_rate = rates[to_currency]
    converted_amount = round(amount * exchange_rate, 2)

    return {
        "amount": amount,
        "from_currency": from_currency,
        "to_currency": to_currency,
        "exchange_rate": exchange_rate,
        "converted_amount": converted_amount
    }

def get_exchange_rates(base_currency: str, currencies: list[str] | None = None) -> dict:
    """Devuelve las tasas de cambio actuales de una moneda base frente a otras.

    Args:
        base_currency: codigo ISO 4217 de la moneda base (p. ej. EUR).
        currencies: lista opcional de codigos a incluir; si se omite, usa
            MONEDAS_HABITUALES.
    """
    if not isinstance(base_currency, str) or base_currency.strip().upper() not in ISO_4217_CODES:
        raise ValueError(f"La moneda base '{base_currency}' debe ser un código ISO 4217 válido.")

    base_currency = base_currency.strip().upper()
    logger.info(f"Obteniendo tasas de cambio para moneda base: {base_currency}")

    all_rates = fetch_exchange_rates(base_currency)
    
    # Determinar qué monedas filtrar (excluyendo la moneda base)
    target_currencies = currencies if currencies is not None else MONEDAS_HABITUALES
    target_currencies = [c.upper() for c in target_currencies if c.upper() != base_currency]

    filtered_rates = {
        curr: all_rates[curr] 
        for curr in target_currencies 
        if curr in all_rates
    }

    return {
        "base_currency": base_currency,
        "rates": filtered_rates
    }