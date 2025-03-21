"""
Module for fetching weather data and handling the Telegram /weather command.
"""

import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

def get_saltney_weather() -> str:
    """Fetch the weather from wx.ja91.uk for Saltney."""
    url = "http://wx.ja91.uk/"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        temperature_element = soup.find(text="Outside Temperature")

        if temperature_element:
            temperature_value = temperature_element.find_next().text.strip()
            return (
                f"Current Outside Temperature in Saltney: {temperature_value}\n"
                f"Provided to you by Jake's Weather Station\nhttp://wx.ja91.uk"
            )

        print("Could not find 'Outside Temperature' on wx.ja91.uk")
        return "Weather data for Saltney is unavailable."
    except requests.RequestException as exc:
        print("Error fetching Saltney weather: %s", exc)
        return "Unable to retrieve Saltney weather at this time."


def get_weather(location: str) -> str:
    """
    Get the current weather for a given location or UK postcode.
    If the location is 'saltney', fetch data from wx.ja91.uk.
    Otherwise, use geocoding APIs and the Open-Meteo weather API.
    """
    if location.lower() == "saltney":
        return get_saltney_weather()

    if location.lower() == "amazingstoke":
        location = "Basingstoke"

    print("Fetching weather for: %s", location)
    geocode_data = None

    # Check if input is a UK postcode (basic pattern matching)
    if location.replace(" ", "").isalnum() and any(char.isdigit() for char in location):
        print("Detected UK postcode, using Nominatim geocoding")
        geocode_url = (
            f"https://nominatim.openstreetmap.org/search?format=json&q={location}, UK"
        )
        geocode_response = requests.get(
            geocode_url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10
        )
        if geocode_response.status_code == 200 and geocode_response.json():
            geocode_data = geocode_response.json()[0]
            latitude = float(geocode_data["lat"])
            longitude = float(geocode_data["lon"])
            print(
                "Geocoded %s to lat: %s, lon: %s", location, latitude, longitude
            )

    if not geocode_data:
        geocode_url = (
            "https://geocoding-api.open-meteo.com/v1/search?"
            f"name={location}&count=1&language=en&format=json"
        )
        geocode_response = requests.get(geocode_url, timeout=10)
        if (
            geocode_response.status_code == 200
            and "results" in geocode_response.json()
        ):
            geocode_data = geocode_response.json()["results"][0]
            latitude = float(geocode_data["latitude"])
            longitude = float(geocode_data["longitude"])
            print(
                "Geocoded %s to lat: %s, lon: %s", location, latitude, longitude
            )

    if not geocode_data:
        print("Location not found: %s", location)
        return "Location not found. Please enter a valid city name or UK postcode."

    weather_url = (
        "https://api.open-meteo.com/v1/forecast?"
        f"latitude={latitude}&longitude={longitude}&current_weather=true"
    )
    weather_response = requests.get(weather_url, timeout=10)
    if weather_response.status_code == 200:
        weather_data = weather_response.json()['current_weather']
        temperature = weather_data['temperature']
        weather_description = "Rainy" if weather_data['weathercode'] in [61, 63, 65, 80, 81, 82] else "Clear/Cloudy"
        print("Weather data: %s°C, Condition: %s", temperature, weather_description)
        return (
            f"Current weather in {location.capitalize()}:\n"
            f"🌡 Temperature: {temperature}°C\n☁ Condition: {weather_description}"
        )
    print("Error fetching weather data: %s, weather_response.text")
    return "Error retrieving weather data. Please try again later."

async def weather_command(update: Update, context: CallbackContext) -> None:
    """Handle the Telegram /weather command."""
    print("Received /weather command from user %s", update.message.from_user.id)
    if not context.args:
        print("No location provided with /weather command")
        await context.bot.send_message(
            chat_id=update.message.chat_id,
            text="Usage: /weather <city or UK postcode>",
        )
        return

    location = " ".join(context.args)
    weather_report = get_weather(location)
    print("Sending weather report for %s", location)
    await context.bot.send_message(
        chat_id=update.message.chat_id, text=weather_report
    )


def register_weather_handler(app: Application) -> None:
    """
    Register the /weather command handler with the given Telegram Application.
    """
    print("Registering /weather command handler")
    app.add_handler(CommandHandler("weather", weather_command))
