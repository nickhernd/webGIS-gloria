#!/bin/bash

# Entrar en entorno
source ../../bin/activate

# This script is used to automate the execution of the program
data_path="../data/"
copernicus_file="copernicus_data.nc"
date_path="data_by_date/"

# Fecha actual
current_date=$(date +'%Y-%m-%d')

log_info() {
		echo -e "\e[32m[INFO]\e[0m $1"
}

error_exit() {
	echo "$1" 1>&2
	exit 1
}

# Exit si un comando falla
set -e

# Exit si un pipe falla
set -e pipefail

trap 'error_exit "[ERROR] El script ha fallado"' ERR

# Comprobamos por si existe ya el archivo copernicus
[ -f $data_path$copernicus_file ] && rm $data_path$copernicus_file

# Obtenemos los datos
log_info "Descargando datos de Copernicus"
python3 obtain_data.py 1> /dev/null
log_info "Datos de Copernicus descargados"

log_info "Procesando datos de Copernicus"
# Convertimos los datos de NetCDF a CSV
log_info "Convirtiendo datos de NetCDF a CSV"
python nc_to_csv.py 1> /dev/null

# Convertimos los datos de CSV a GeoJSON
log_info "Convirtiendo datos de CSV a GeoJSON"
python csv_to_json.py
log_info "Datos procesados correctamente"

# Si existe la carpeta la eliminamos
[ -d $data_path$date_path ] && rm -r $data_path$date_path && mkdir $data_path$date_path

# Separamos la información por fecha
log_info "Separamos los datos por fecha"
python separate_by_date.py
log_info "Separado correctamente por fecha"

# Guardamos la fecha actual en las piscifactorías
log_info "Guardamos la fecha actual en las piscifactorías"
python search_wave_by_coord_recinto.py date $current_date
python insert_wave_into_recinto.py
log_info "Fecha guardada correctamente"


