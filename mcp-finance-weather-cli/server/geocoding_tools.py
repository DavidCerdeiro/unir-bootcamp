"""Herramienta de geocodificacion (Open-Meteo): ciudad -> coordenadas."""

import logging

from server.api_clients import fetch_geocoding

logger = logging.getLogger(__name__)


def geocode_city(city: str) -> dict:
    """Devuelve las coordenadas y datos basicos de una ciudad por su nombre.

    Args:
        city: nombre de la ciudad (p. ej. Madrid, Nueva York, Tokio).
    """
    if not city or not str(city).strip():
        raise ValueError("El nombre de la ciudad es obligatorio y no puede estar vacío.")

    city_cleaned = str(city).strip()
    logger.info(f"Geocodificando ciudad: {city_cleaned}")
    
    # Asumimos que fetch_geocoding extrae el primer/mejor resultado y lanza excepción si no hay matches.
    data = fetch_geocoding(city_cleaned)
    
    return {
        "city": data.get("name", city_cleaned),
        "latitude": data.get("latitude"),
        "longitude": data.get("longitude"),
        "country": data.get("country", "Desconocido"),
        "timezone": data.get("timezone", "UTC")
    }