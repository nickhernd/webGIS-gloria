# Estudio entorno GIS en piscifactorias

En este estudio se explicará la creación de una webGIS para piscifactorías, esto tiene como finalidad el facilitar información a los trabajadores pesqueros sobre las piscifactorías en la costa Mediterranea. Acompañado del estudio de Gloria2 que observa diferente información marítima como es la altura de la ola, el fin es crear una webGIS que pueda representar esta información creando una representando una predicción temporal del riesgo de escape de peces en susodicho. 

## Investigación previa

Para la obtención de la información se han mirado diferentes proveedores de datos que nos proporcionen parámetros temporales sobre el mar. El primero es ECMWF que es TODO COMPLETAR

En cambio, CopernicusMarine TODO ...

Se ha escogido CopernicusMarine porque varias razones. La primera es que es más fácil conseguir la información que queremos, teniendo una librería de python con la cual podremos obtener la información de forma mas sencilla. La segunda es que proporciona la información de manera gratuita, es verdad que ECMWF tiene su parte gratuita pero sus bases de datos requieren unos permisos de acceso que se obtienen por pagando los datos. 

## Arquitectura 

La webGIS está basada en una base estructural rodeada de un servidor linux que maneja el flujo del server automatizándolo con crontab, facilitando la obtención, conversión, limpieza y procesamiento de los datos con python y bash scripting. Guarda la información en un formato GeoJSON, pasando del tipo de archivo NetCDF a CSV, y de CSV a GeoJSON. Por otra parte, se procesa y convierte los datos de las piscifactorías convirtiéndolo a GeoJSON. Toda esta información GeoJSON la manejamos y desplegamos con Node JS a un servidor que publicamos en la red, que con la librería de Mapbox JS representará la información de manera visual.

### Obtención y procesamiento de la información de CopernicusMarine

Para la obtención de la información primero llamamos a la API de CopernicusMarine, obtenemos la información de la base de datos TODO.
