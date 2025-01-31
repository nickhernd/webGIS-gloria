import unittest
from pathlib import Path
import sys
import os

# Añadir el directorio raíz al path
ROOT_DIR = Path(__file__).parent.parent.parent
sys.path.append(str(ROOT_DIR))

from scripts.pipeline.test_pipeline import DataPipeline

class TestPipeline(unittest.TestCase):
    def setUp(self):
        """Configuración inicial para cada test"""
        self.pipeline = DataPipeline()

    def test_pipeline_initialization(self):
        """Probar que el pipeline se inicializa correctamente"""
        self.assertIsNotNone(self.pipeline)
        self.assertIsNotNone(self.pipeline.root_dir)
        self.assertIsNotNone(self.pipeline.data_dir)
        self.assertIsNotNone(self.pipeline.config)

    def test_directories_exist(self):
        """Probar que los directorios necesarios existen"""
        required_dirs = [
            self.pipeline.data_dir / 'raw' / 'copernicus',
            self.pipeline.data_dir / 'raw' / 'geographic',
            self.pipeline.data_dir / 'processed' / 'daily',
            self.pipeline.data_dir / 'processed' / 'geographic',
            self.pipeline.data_dir / 'processed' / 'weather',
            self.pipeline.data_dir / 'processed' / 'analysis',
            self.pipeline.data_dir / 'temp',
        ]
        
        for directory in required_dirs:
            self.assertTrue(
                directory.exists(), 
                f"Directorio no encontrado: {directory}"
            )

    def test_config_loading(self):
        """Probar que la configuración se carga correctamente"""
        config = self.pipeline._cargar_config()
        
        # Verificar que existen las claves necesarias
        self.assertIn('copernicus', config)
        self.assertIn('openweather', config)
        self.assertIn('coordinates', config)
        self.assertIn('time_range', config)

        # Verificar estructura de coordenadas
        coords = config['coordinates']
        self.assertIn('minlon', coords)
        self.assertIn('maxlon', coords)
        self.assertIn('minlat', coords)
        self.assertIn('maxlat', coords)

if __name__ == '__main__':
    unittest.main()
