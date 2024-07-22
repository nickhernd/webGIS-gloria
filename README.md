# Cuadro de mando aplicado a las piscifactorías.

## Introducción

Esto es un proyecto creado por Sebastian Pasker. Con autores a Javier Atalah y Andrés Fuster para el trabajo de fin de grado de la carrera de Ingeniería Informática en la Universidad de Alicante. Esto es la segunda parte del trabajo de 'Sistemas de información geográfica para la gestión de datos en entornos pesqueros y acuicultores'. 

En este proyecto se representa factores de riesgo de escape de los peces como la altura de la ola para determinar con una visualización en escala por cada piscifactoría de la costa mediterránea.

## Instalación

Para su instalación, se recomienda realizarlo en un entorno python. Para ello, se recomienda instalar un entorno virtual con el siguiente comando:

```bash
python3 -m venv venv
```

Una vez creado el entorno virtual, se debe activar con el siguiente comando:

```bash
source venv/bin/activate
```

Una vez activado el entorno virtual, se debe instalar las dependencias necesarias con el siguiente comando:

```bash
pip install -r dependencies.txt
```

Para necesitará tener los datos necesarios de las coordenadas de las piscifactorías y otras cosas como la api key de mapbox y la api key de openweathermap para poder visualizar los datos en el mapa.

## Automatización en Cron

Para automatizar la ejecución del script, se puede utilizar el cron de linux. Para ello, se debe ejecutar el siguiente comando:

```bash
crontab -e
```

Una vez dentro del editor de texto, se debe añadir la siguiente línea para ejecutar el script cada 24 horas a las 00:00:

```bash
0 0 * * * /path/to/tfg/scriptsº/automate_execution.bash
```
