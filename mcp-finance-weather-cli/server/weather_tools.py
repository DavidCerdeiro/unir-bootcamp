"""Herramientas de clima (Open-Meteo): requieren coordenadas (lat/lon)."""

import logging

from server.api_clients import describe_weather_code, fetch_current_weather, fetch_forecast

logger = logging.getLogger(__name__)


def _validate_coordinates(latitude: float, longitude: float) -> None:
    """Valida que las coordenadas estén dentro de los rangos geográficos reales."""
    if not isinstance(latitude, (int, float)) or not (-90.0 <= latitude <= 90.0):
        raise ValueError(f"Latitud inválida ({latitude}). Debe estar entre -90 y 90 grados.")
    if not isinstance(longitude, (int, float)) or not (-180.0 <= longitude <= 180.0):
        raise ValueError(f"Longitud inválida ({longitude}). Debe estar entre -180 y 180 grados.")


def get_current_weather(latitude: float, longitude: float) -> dict:
    """Devuelve el clima actual para unas coordenadas.

    Args:
        latitude: latitud en grados decimales (-90 a 90).
        longitude: longitud en grados decimales (-180 a 180).
    """
    _validate_coordinates(latitude, longitude)
    
    logger.info(f"Consultando clima actual para coordenadas: {latitude}, {longitude}")
    data = fetch_current_weather(latitude, longitude)
    
    # Asumiendo que fetch_current_weather devuelve un diccionario normalizado
    # o directamente el nodo "current" / "current_weather" de Open-Meteo.
    weather_code = data.get("weather_code", data.get("weathercode", 0))
    
    return {
        "temperatura": data.get("temperature_2m", data.get("temperature")),
        "sensacion_termica": data.get("apparent_temperature", data.get("feels_like")),
        "humedad": data.get("relative_humidity_2m", data.get("humidity")),
        "viento": data.get("wind_speed_10m", data.get("windspeed")),
        "descripcion": describe_weather_code(weather_code)
    }


def get_weather_forecast(latitude: float, longitude: float, days: int = 5) -> dict:
    """Devuelve el pronostico diario para unas coordenadas.

    Args:
        latitude: latitud en grados decimales (-90 a 90).
        longitude: longitud en grados decimales (-180 a 180).
        days: numero de dias de pronostico (1 a 7).
    """
    _validate_coordinates(latitude, longitude)
    
    if not isinstance(days, int) or not (1 <= days <= 7):
        raise ValueError(f"El número de días ({days}) debe ser un entero entre 1 y 7.")

    logger.info(f"Consultando pronóstico de {days} días para coordenadas: {latitude}, {longitude}")
    forecast_data = fetch_forecast(latitude, longitude, days)
    
    dias_procesados = []
    
    # Manejo robusto dependiendo de cómo formatea la respuesta fetch_forecast.
    # Si devuelve el nodo 'daily' nativo de Open-Meteo (diccionario de listas de la misma longitud):
    if isinstance(forecast_data, dict) and "time" in forecast_data:
        for i, date_str in enumerate(forecast_data["time"]):
            w_code = forecast_data.get("weather_code", [0]*(i+1))[i]
            dias_procesados.append({
                "fecha": date_str,
                "maxima": forecast_data.get("temperature_2m_max", [None]*(i+1))[i],
                "minima": forecast_data.get("temperature_2m_min", [None]*(i+1))[i],
                "probabilidad_precipitacion": forecast_data.get("precipitation_probability_max", [None]*(i+1))[i],
                "descripcion": describe_weather_code(w_code)
            })
    # Si ya viene preprocesado como una lista de diccionarios desde api_clients:
    elif isinstance(forecast_data, list):
        for item in forecast_data:
            w_code = item.get("weather_code", item.get("weathercode", 0))
            dias_procesados.append({
                "fecha": item.get("fecha", item.get("time")),
                "maxima": item.get("maxima", item.get("temperature_2m_max")),
                "minima": item.get("minima", item.get("temperature_2m_min")),
                "probabilidad_precipitacion": item.get("probabilidad_precipitacion", item.get("precipitation_probability_max")),
                "descripcion": describe_weather_code(w_code)
            })
    else:
        # Fallback en caso de formato inesperado
        return {"days": forecast_data}

    return {"days": dias_procesados}