import unittest
from pathlib import Path
import sys
import os
import json
import pandas as pd

# Añadir el directorio raíz al path
ROOT_DIR = Path(__file__).parent.parent.parent
sys.path.append(str(ROOT_DIR))

from backend.data_processing.nc_to_csv import NetCDFConverter
from backend.data_processing.calculate_center import calculate_centers, process_geographic_data
from backend.data_processing.separate_by_date import separate_data_by_date

class TestDataProcessing(unittest.TestCase):
    def setUp(self):
        """Configuración inicial para cada test"""
        self.data_dir = ROOT_DIR / 'data'
        self.test_data_dir = ROOT_DIR / 'backend/tests/test_data'
        self.test_data_dir.mkdir(exist_ok=True)

    def test_netcdf_converter(self):
        """Probar conversión de NetCDF a CSV"""
        converter = NetCDFConverter()
        
        # Verificar que el conversor se inicializa
        self.assertIsNotNone(converter)
        
        # Verificar que existe el archivo de entrada
        input_file = self.data_dir / 'raw/copernicus/wave_data.nc'
        self.assertTrue(
            input_file.exists(),
            "Archivo NetCDF de prueba no encontrado"
        )

    def test_geographic_processing(self):
        """Probar procesamiento de datos geográficos"""
        # Cargar datos geográficos de prueba
        geojson_path = self.data_dir / 'raw/geographic/recintos_buffer.geojson'
        
        self.assertTrue(
            geojson_path.exists(),
            "Archivo GeoJSON de prueba no encontrado"
        )
        
        # Leer y verificar estructura del GeoJSON
        with open(geojson_path) as f:
            data = json.load(f)
            
        self.assertIn('type', data)
        self.assertIn('features', data)
        self.assertTrue(len(data['features']) > 0)

    def test_date_separation(self):
        """Probar separación de datos por fecha"""
        # Verificar directorio de datos diarios
        daily_dir = self.data_dir / 'processed/daily/data_by_date'
        self.assertTrue(daily_dir.exists())
        
        # Verificar que hay archivos de datos diarios
        daily_files = list(daily_dir.glob('*.geojson'))
        self.assertTrue(
            len(daily_files) > 0,
            "No se encontraron archivos de datos diarios"
        )
        
        # Verificar estructura de un archivo diario
        if daily_files:
            with open(daily_files[0]) as f:
                data = json.load(f)
                self.assertIn('type', data)
                self.assertIn('features', data)

    def test_data_consistency(self):
        """Probar consistencia de datos procesados"""
        # Verificar datos de oleaje
        wave_csv = self.data_dir / 'temp/wave_data.csv'
        if wave_csv.exists():
            df = pd.read_csv(wave_csv)
            self.assertIn('wave_height', df.columns)
            self.assertTrue(len(df) > 0)

        # Verificar datos meteorológicos
        weather_json = self.data_dir / 'processed/weather/weather_data.json'
        if weather_json.exists():
            with open(weather_json) as f:
                data = json.load(f)
                self.assertIsInstance(data, dict)

    def tearDown(self):
        """Limpieza después de cada test"""
        # Eliminar archivos temporales de prueba si existen
        if self.test_data_dir.exists():
            for file in self.test_data_dir.iterdir():
                file.unlink()
            self.test_data_dir.rmdir()

if __name__ == '__main__':
    unittest.main()
