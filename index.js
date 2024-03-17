const express = require("express");
const app = express();
const path = require('path');
const bodyParser = require('body-parser');
const { readFileSync } = require('fs');

let port = process.env.PORT || 8080;
let host = 'localhost';

app.set('port', (port));
app.use(express.static(__dirname + '/public'));
app.set('views', __dirname + "/public/views");
app.engine('html', require('ejs').renderFile)
app.set('view engine', 'html')


let json_coordinates_path = __dirname + "/data/coord_lonjas.json";
let json_fish_farm_path = __dirname + "/data/recintos_buffer.geojson";

var json_coordinates_data = readFileSync(json_coordinates_path);
var json_fish_farm_data = readFileSync(json_fish_farm_path);

app.get("/", function(req, res) {
	parsed_coordinates = JSON.parse(json_coordinates_data);
	parsed_fish_farm = JSON.parse(json_fish_farm_data);

	res.render("index.html", {data : JSON.stringify(parsed_coordinates), data_fish_farm : JSON.stringify(parsed_fish_farm)})
})


app.listen(port, function() {
	console.log("Start", port)
})
