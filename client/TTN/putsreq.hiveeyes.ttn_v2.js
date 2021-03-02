// -------------------------------
// Hiveeyes
// https://swarm.hiveeyes.org/api/
// -------------------------------

const input = JSON.parse(request.body);

var output  = {};

output    = input.payload_fields;
output.sf = Number(input.metadata.data_rate.split('BW')[0].substring(2));
output.bw = Number(input.metadata.data_rate.split('BW')[1]);
output.gtw_count = Number(input.metadata.gateways.length);

for (i = 0; i < input.metadata.gateways.length; i++) {
  output["gw_" + input.metadata.gateways[i].gtw_id + "_rssi"] = input.metadata.gateways[i].rssi;
  output["gw_" + input.metadata.gateways[i].gtw_id + "_snr"]  = input.metadata.gateways[i].snr;
}

const URL = "https://swarm.hiveeyes.org/api/" + input.dev_id.replace(/-/g, '/') + "/data";

request.body = output;
request.forwardTo = URL;
