function get_wave_by_hour_str(feature, hour) {
	// Convertimos el string de waves en un array
	var waves = feature.properties.wave_height.slice(1, feature.properties.wave_height.length-1).split(",");
	// Quitamos espacios y las comillas laterales
	waves = waves.map(function(wave) {
		return wave.trim().slice(1, wave.length-1);
	});

	// Convertimos el string de date and time en un array
	var dates = feature.properties.time.slice(1, feature.properties.time.length-1).split(",");
	// Quitamos espacios y las comillas laterales
	dates = dates.map(function(date) {
		return date.trim().slice(1, date.length-1);
	});
	// Quitamos los valores de la fecha
	dates = dates.map(function(date) {
		return date.split(" ")[1];
	});
	var hours = dates.map(function(hour) {
		return hour.split(":")[0];
	})
	// Buscamos la hora en el array de fechas y nos quedamos con el indice
	var index = hours.indexOf(hour.split(":")[0]);

	// Devolvemos el valor de la ola en la misma posición
	return { waves, index };
}

function get_wave_by_hour(feature, hour) {
	// Buscamos la hora en el array de fechas y nos quedamos con el indice
	var index = feature.properties.time.map(function(time_t) {
		return time_t.split(" ")[1];
	}).map(function(hour_t) {
		return hour_t.split(":")[0];
	}).indexOf(hour.split(":")[0]);

	return index
}

module.exports = get_wave_by_hour;
