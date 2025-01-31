#!/usr/bin/env python3
import os
from getpass import getpass
from pathlib import Path
from dotenv import load_dotenv, set_key

def setup_copernicus_credentials():
    """Configurar credenciales de Copernicus Marine"""
    env_file = Path('.env')
    
    # Crear .env si no existe
    if not env_file.exists():
        env_file.touch()
        
    # Cargar variables de entorno existentes
    load_dotenv()
    
    # Solicitar credenciales
    username = input("Introduce tu usuario de Copernicus Marine: ")
    password = getpass("Introduce tu contraseña de Copernicus Marine: ")
    
    # Guardar en .env
    set_key('.env', 'COPERNICUS_USERNAME', username)
    set_key('.env', 'COPERNICUS_PASSWORD', password)
    
    print("\nCredenciales guardadas correctamente en .env")
    
if __name__ == "__main__":
    setup_copernicus_credentials()
