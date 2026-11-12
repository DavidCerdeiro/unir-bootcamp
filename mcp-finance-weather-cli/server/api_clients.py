"""Clientes HTTP para las APIs externas (ExchangeRate-API y Open-Meteo)."""

import logging
import requests
from config import settings

logger = logging.getLogger(__name__)

class ApiClientError(Exception):
    """Error controlado al consultar una API externa."""

def _get_json(url: str, params: dict | None = None) -> dict:
    """GET con timeout y errores de red convertidos a ApiClientError."""
    try:
        # Por seguridad asumimos 10 segundos si settings.HTTP_TIMEOUT no está definido
        timeout = getattr(settings, 'HTTP_TIMEOUT', 10)
        response = requests.get(url, params=params, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except requests.Timeout as error:
        raise ApiClientError(f"Timeout consultando {url}") from error
    except requests.HTTPError as error:
        status = error.response.status_code if error.response is not None else "?"
        raise ApiClientError(f"La API devolvió HTTP {status} para {url}") from error
    except requests.RequestException as error:
        raise ApiClientError(f"Error de red consultando {url}: {error}") from error
    except ValueError as error:
        raise ApiClientError(f"Respuesta no válida (no es JSON) de {url}") from error


def fetch_exchange_rates(base_currency: str) -> dict[str, float]:
    """Devuelve las tasas de cambio actuales para una moneda base."""
    api_key = getattr(settings, "API_KEY_EXCHANGE", None)
    
    if api_key:
        base_url = getattr(settings, "BASE_URL_EXCHANGE_V6", "https://v6.exchangerate-api.com/v6")
        url = f"{base_url}/{api_key}/latest/{base_currency}"
        rates_key = "conversion_rates"
    else:
        # Fallback abierto en caso de no proveer la clave
        base_url = getattr(settings, "BASE_URL_EXCHANGE_OPEN", "https://open.er-api.com/v6")
        url = f"{base_url}/latest/{base_currency}"
        rates_key = "rates"

    data = _get_json(url)

    if data.get("result") != "success":
        raise ApiClientError(f"La API de conversión de monedas falló. Resultado: {data.get('result')}")
    
    return data.get(rates_key, {})


def fetch_geocoding(city: str) -> dict:
    """Devuelve el primer resultado de geocodificación para una ciudad."""
    base_url = getattr(settings, "BASE_URL_GEOCODING", "https://geocoding-api.open-meteo.com/v1/search").rstrip('/')
    url = f"{base_url}"
    
    params = {
        "name": city,
        "count": 1,
        "language": "es",
        "format": "json"
    }
    
    data = _get_json(url, params=params)
    results = data.get("results")
    
    if not results:
        raise ApiClientError(f"No se han encontrado resultados de geocodificación para la ciudad: '{city}'")
        
    return results[0]


def fetch_current_weather(latitude: float, longitude: float) -> dict:
    """Devuelve el bloque de clima actual de Open-Meteo para unas coordenadas."""
    base_url = getattr(settings, "BASE_URL_WEATHER", "https://api.open-meteo.com/v1").rstrip('/')
    url = f"{base_url}/forecast"
    
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,wind_speed_10m",
        "timezone": "auto"
    }
    
    data = _get_json(url, params=params)
    
    if "current" not in data:
        raise ApiClientError("La respuesta de la API meteorológica no contiene el bloque 'current'.")
        
    return data["current"]


def fetch_forecast(latitude: float, longitude: float, days: int) -> dict:
    """Devuelve el bloque diario de pronóstico de Open-Meteo."""
    base_url = getattr(settings, "BASE_URL_WEATHER", "https://api.open-meteo.com/v1").rstrip('/')
    url = f"{base_url}/forecast"
    
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_probability_max,weather_code",
        "forecast_days": days,
        "timezone": "auto"
    }
    
    data = _get_json(url, params=params)
    
    if "daily" not in data:
        raise ApiClientError("La respuesta de la API meteorológica no contiene el bloque 'daily'.")
        
    return data["daily"]


# Descripciones en español de los codigos meteorologicos WMO de Open-Meteo.
WEATHER_CODES: dict[int, str] = {
    0: "cielo despejado",
    1: "principalmente despejado",
    2: "parcialmente nublado",
    3: "cubierto",
    45: "niebla",
    48: "niebla con escarcha",
    51: "llovizna ligera",
    53: "llovizna moderada",
    55: "llovizna intensa",
    61: "lluvia ligera",
    63: "lluvia moderada",
    65: "lluvia intensa",
    71: "nieve ligera",
    73: "nieve moderada",
    75: "nieve intensa",
    80: "chubascos ligeros",
    81: "chubascos moderados",
    82: "chubascos violentos",
    95: "tormenta",
    96: "tormenta con granizo ligero",
    99: "tormenta con granizo intenso",
}

def describe_weather_code(code: int | None) -> str:
    """Traduce un código WMO a una descripción legible en español."""
    if code is None:
        return "sin datos"
    return WEATHER_CODES.get(int(code), f"código WMO {code}")