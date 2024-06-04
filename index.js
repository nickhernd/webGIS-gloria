const bodyParser = require('body-parser');
const express = require("express");
const app = express();
const execSync = require('child_process').execSync
const path = require('path');
const url = require('url');
const { readFileSync } = require('fs');
const associate_wave_with_geojson = require('./public/js/associate_wave_with_geojson.js')

let port = process.env.PORT || 8080;
let host = 'localhost';
app.set('port', (port));
app.use(express.static(__dirname + '/public'));
app.set('views', __dirname + "/public/views");
app.engine('html', require('ejs').renderFile)
app.set('view engine', 'html')

app.use(express.urlencoded({ extended: true  }));

let json_coordinates_path = __dirname + "/data/coord_lonjas.json";
let json_fish_farm_path = __dirname + "/data/recintos_with_openweather.geojson";


app.get("/", function(req, res) {
	var json_coordinates_data = readFileSync(json_coordinates_path);
	var json_fish_farm_data = readFileSync(json_fish_farm_path);
	parsed_coordinates = JSON.parse(json_coordinates_data);
	parsed_fish_farm = JSON.parse(json_fish_farm_data);

	var hora = "00:00"
	if(req.query.hour != undefined) {
		hora = req.query.hour
	}

	if(req.query.date != undefined) {
		date = req.query.date
	} else {
		// Obtenemos la fecha actual
		const currentDate = new Date();
		const year = currentDate.getFullYear();
		const month = String(currentDate.getMonth() + 1).padStart(2, '0');
		const day = String(currentDate.getDate()).padStart(2, '0');
		const formattedDate = `${year}-${month}-${day}`;
		date = formattedDate
	}

	var parsed_fish_farm_hour = associate_wave_with_geojson(parsed_fish_farm, hora)

	res.render("index.html", {data : JSON.stringify(parsed_coordinates), data_fish_farm : JSON.stringify(parsed_fish_farm_hour), hora : hora, fecha : date})
})


function validarFormatoFecha(fecha) {
    // Expresión regular para el formato 'Y-m-d'
    const regex = /^\d{4}-\d{2}-\d{2}$/i;
    return regex.test(fecha);
}

app.post("/", function(req, res) {
	var date=req.body.fecha
	var hour=req.body.hora

	if(!validarFormatoFecha(date)) {
		res.status(400).send("La fecha no tiene el formato correcto");
		return;
	}

	search_date_command = 'python search_wave_by_coord_recinto.py date '
	insert_wave_command = 'python insert_wave_into_recinto.py'
	command = 'cd scripts && ' + search_date_command + date + ' && ' + insert_wave_command

	try {
		run_command = execSync(command)
	} catch(err) {

		console.log("Error:")
		console.log("Output: ", err)
		console.log("Stderr: ", err.stderr.toString())
		res.status(500).send("Error al ejecutar el comando")
	}
	
	if(req.session == undefined) {
		req.session = {}
	}

	query = {}
	if(hour != undefined) {
		query["hour"] = hour
	}
	if(date != undefined) {
		query["date"] = date
	}

	if(hour != undefined || date != undefined) {
		res.redirect(url.format({
			pathname:"/",
			query: query
		}))
	} else {
		res.redirect("/")
	}
})

app.get("/wave_med", function(req, res) {
	res.sendFile(path.resolve(__dirname + "/data/wave_med.nc"))
})



app.listen(port, function() {
	console.log("Start", port)
})
