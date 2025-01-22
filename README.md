# Cuadro de mando aplicado a las piscifactorías.

## Introducción

Esto es un proyecto creado por Sebastian Pasker. Con autores a Javier Atalah y Andrés Fuster para el trabajo de fin de grado de la carrera de Ingeniería Informática en la Universidad de Alicante. Esto es la segunda parte del trabajo de 'Sistemas de información geográfica para la gestión de datos en entornos pesqueros y acuicultores'.

En este proyecto se representa factores de riesgo de escape de los peces como la altura de la ola para determinar con una visualización en escala por cada piscifactoría de la costa mediterránea.

## Instalación

### Ejecución local con Node.js

Para ejecutar el proyecto localmente con Node.js, sigue estos pasos:

1. Asegúrate de tener Node.js instalado en tu sistema. Puedes verificarlo ejecutando:

   ```bash
   node -v
   ```

   Si no está instalado, descárgalo desde [Node.js](https://nodejs.org/) e instálalo.

2. Navega al directorio principal del proyecto y ejecuta el siguiente comando:

   ```bash
   node index.js
   ```

   Esto iniciará el proyecto localmente.

### Configuración de claves y credenciales

Dentro del proyecto, hay una carpeta llamada `keys/` que contiene los siguientes archivos:

- `api_openweather.txt`: Debes agregar tu clave API de OpenWeather en este archivo.
- `cmems_credentials.json`: Este archivo contiene las credenciales para CMEMS (Copernicus Marine Environment Monitoring Service). Necesitarás completarlo con tu usuario y contraseña.

Asegúrate de que ambos archivos estén correctamente configurados antes de ejecutar el proyecto.

### Configuración del entorno en Python

Para su instalación en Python, se recomienda realizarlo en un entorno virtual. Para ello, sigue estos pasos:

1. Crea un entorno virtual:

   ```bash
   python3 -m venv venv
   ```

2. Activa el entorno virtual:

   ```bash
   source venv/bin/activate
   ```

3. Instala las dependencias necesarias:

   ```bash
   pip install -r dependencies.txt
   ```

Es necesario tener los datos requeridos como las coordenadas de las piscifactorías y las claves API de servicios como Mapbox y OpenWeather para la visualización de los datos en el mapa.

## Automatización en Cron

Para la extracción de información de manera asincrónica, se incluye el script `automate_execution.bash`. Sigue estos pasos para configurarlo:

1. Da permisos de ejecución al script:

   ```bash
   chmod +x automate_execution.bash
   ```

2. Ejecûtalo manualmente si es necesario:

   ```bash
   ./automate_execution.bash
   ```

3. Para automatizar su ejecución usando Cron en Linux, edita el crontab:

   ```bash
   crontab -e
   ```

   Añade la siguiente línea para ejecutarlo cada 24 horas a las 00:00:

   ```bash
   0 0 * * * /path/to/tfg/scripts/automate_execution.bash
   ```

## Más información

Para más detalles, consulta la segunda parte de `memoria_tfg.pdf` o contacta con Sebastian Pasker en [sebaspasker@gmail.com](mailto:sebaspasker@gmail.com).

