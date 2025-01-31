from fastapi.testclient import TestClient
import unittest
from pathlib import Path
import sys
import json

# Añadir el directorio raíz al path
ROOT_DIR = Path(__file__).parent.parent.parent
sys.path.append(str(ROOT_DIR))

from backend.api.main import app

class TestAPIs(unittest.TestCase):
    def setUp(self):
        """Configuración inicial para cada test"""
        self.client = TestClient(app)
        self.data_dir = ROOT_DIR / 'data'

    def test_farms_endpoint(self):
        """Test del endpoint de piscifactorías"""
        response = self.client.get("/api/farms/geojson")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('type', data)
        self.assertIn('features', data)

    def test_wave_data_endpoint(self):
        """Test del endpoint de datos de oleaje"""
        response = self.client.get("/api/wave-data")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('labels', data)
        self.assertIn('values', data)

    def test_weather_data_endpoint(self):
        """Test del endpoint de datos meteorológicos"""
        response = self.client.get("/api/weather-data")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, dict)

    def test_alerts_endpoint(self):
        """Test del endpoint de alertas"""
        response = self.client.get("/api/alerts")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)

    def test_pipeline_status_endpoint(self):
        """Test del endpoint de estado del pipeline"""
        response = self.client.get("/api/pipeline/status")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('running', data)
        self.assertIn('status', data)

    def test_farm_details_endpoint(self):
        """Test del endpoint de detalles de piscifactoría"""
        # Primero obtenemos el ID de una piscifactoría
        response = self.client.get("/api/farms/geojson")
        farms_data = response.json()
        if farms_data['features']:
            farm_id = farms_data['features'][0]['properties']['id']
            response = self.client.get(f"/api/farms/{farm_id}")
            self.assertEqual(response.status_code, 200)

    def test_error_handling(self):
        """Test de manejo de errores"""
        # Probar ID no existente
        response = self.client.get("/api/farms/nonexistent_id")
        self.assertEqual(response.status_code, 404)

        # Probar ruta no existente
        response = self.client.get("/api/nonexistent_route")
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
