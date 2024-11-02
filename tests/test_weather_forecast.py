import unittest
from unittest.mock import patch
from fpdf import FPDF

from agent_ai_project.weather_data_8days import get_weather_data, extract_forecast_info, save_forecast_to_pdf

class TestWeatherForecast(unittest.TestCase):

    def setUp(self):
        # Przygotowanie przykładowych danych pogodowych
        self.sample_weather_data = {
            "list": [
                {
                    "dt_txt": "2024-11-01 09:00:00",
                    "main": {
                        "feels_like": 15.0,
                    },
                    "wind": {
                        "speed": 5.0,
                    },
                    "weather": [
                        {"description": "clear sky"}
                    ]
                },
                {
                    "dt_txt": "2024-11-01 15:00:00",
                    "main": {
                        "feels_like": 18.0,
                    },
                    "wind": {
                        "speed": 3.0,
                    },
                    "weather": [
                        {"description": "partly cloudy"}
                    ]
                },
                {
                    "dt_txt": "2024-11-01 21:00:00",
                    "main": {
                        "feels_like": 12.0,
                    },
                    "wind": {
                        "speed": 2.0,
                    },
                    "weather": [
                        {"description": "light rain"}
                    ]
                }
            ]
        }

    @patch('weather_data_8days.requests.get')
    def test_get_weather_data(self, mock_get):
        # Ustawienie odpowiedzi mock
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = self.sample_weather_data

        lat, lon = 52.2297, 21.0122  # Przykładowe współrzędne
        result = get_weather_data(lat, lon)
        self.assertEqual(result, self.sample_weather_data, "Powinno zwrócić poprawne dane pogodowe")

    def test_extract_forecast_info(self):
        city_name = "Warsaw"
        forecast_info = extract_forecast_info(self.sample_weather_data, city_name)

        expected_output = {
            "2024-11-01": [
                "Morning: Date: 2024-11-01 - Feels like: 15.0°C, Wind speed: 5.0 m/s, Overall forecast: Clear sky",
                "Afternoon: Date: 2024-11-01 - Feels like: 18.0°C, Wind speed: 3.0 m/s, Overall forecast: Partly cloudy",
                "Evening: Date: 2024-11-01 - Feels like: 12.0°C, Wind speed: 2.0 m/s, Overall forecast: Light rain"
            ]
        }

        self.assertEqual(forecast_info, expected_output, "Powinno zwrócić poprawnie przetworzone prognozy")

    def test_save_forecast_to_pdf(self):
        pdf = save_forecast_to_pdf(self.sample_weather_data, "Warsaw")

        # Sprawdzanie, czy PDF został poprawnie stworzony
        self.assertIsInstance(pdf, FPDF, "Powinno zwrócić instancję FPDF")

if __name__ == '__main__':
    unittest.main()
