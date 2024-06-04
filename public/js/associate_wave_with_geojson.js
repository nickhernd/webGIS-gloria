const get_wave_by_hour = require('./get_wave_by_hour.js')

function associate_wave_with_geojson(geojson, hour) {
	var index = get_wave_by_hour(geojson.features[0], hour)

	test = 0.0
	geojson.features.forEach(function(feature) {
	 // feature.properties.wave_hour = parseFloat(feature.properties.wave_height[index])
	 feature.properties.wave_hour = test 
	 test += 0.5
	})


	return geojson
}

module.exports = associate_wave_with_geojson
