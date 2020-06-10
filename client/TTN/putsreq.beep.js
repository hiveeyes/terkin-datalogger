// -------------------------------
// B E E P
// https://api.beep.nl/api/sensors
// -------------------------------

const input = JSON.parse(request.body);
const payload_ttn = input.payload_fields;

var input_beep   = {};
var output_beep  = "";
var beep_key     = "";

// map TTN device IDs to BEEP keys
switch (input.dev_id) {
    case "hiveeyes-USER-LOCATION-NAMEOFHIVE":
        output_bob.key = "YOUR-BOB-KEY-FOR-NODE-A";
        break;
    case "hiveeyes-USER-LOCATION-NAMEOFHIVE":
        output_bob.key = "YOUR-BOB-KEY-FOR-NODE-B";
        break;
}

// base URL with BEEP key
output_beep = "https://api.beep.nl/api/sensors?key=" + beep_key;

// parse TTN payload into input_beep
for (var key in payload_ttn) {
    if (payload_ttn.hasOwnProperty(key)) {
        if (/load/.test(key)) {
            input_beep.weight_kg = payload_ttn[key];
        } else if (/temperature_5/.test(key)) {
            input_beep.t = payload_ttn[key];
        } else if (/relative_humidity_5/.test(key)) {
            input_beep.h = payload_ttn[key];
        } else if (/barometric_pressure_5/.test(key)) {
            input_beep.p = payload_ttn[key];
        } else if (/voltage_0/.test(key)) {
            input_beep.bv = payload_ttn[key];
        } else if (/temperature_10/.test(key)) {
//            i = parseInt(key.split("_")[1],10);
//            output_bob["t_i" + (i-9)] = payload_ttn[key];
            input_beep.t_i = payload_ttn[key];
        }
    }
}

// take RSSI and SNR from first gateway in JSON
input_beep.rssi = input.metadata.gateways[0].rssi;
input_beep.snr  = input.metadata.gateways[0].snr;

// overwrite RSSI and SNR if a gateway with better RSSI value is reported
for (i = 1; i < input.metadata.gateways.length; i++) {
  if (input.metadata.gateways[i].rssi > input_beep.rssi) {
      input_beep.rssi = input.metadata.gateways[i].rssi;
      input_beep.snr = input.metadata.gateways[i].snr;
    }
}

// create URL parameters
for (var value_key in input_beep) {
    output_beep += "&" + value_key + "=" + input_beep[value_key];
}

// set HTTP header
request.headers['Content-Type'] = 'application/x-www-form-urlencoded';

// Forward a request
request.forwardTo = output_beep;
