// -------------------------------
// Hiveeyes
// https://swarm.hiveeyes.org/api/
// -------------------------------

const input = JSON.parse(request.body);

var output = {};

output      = input.uplink_message.decoded_payload;
output.sf   = input.uplink_message.settings.data_rate.lora.spreading_factor;
output.bw   = input.uplink_message.settings.data_rate.lora.bandwidth / 1000;
output.freq = input.uplink_message.settings.frequency / 1000000.0;
output.counter = input.uplink_message.f_cnt;
output.gtw_count = input.uplink_message.rx_metadata.length;

/* ToDo: use gateway ID instead of array index once it is included in the TTN payload.
   Perhaps when uplinks route directly via V3 Gateways */
for (i = 0; i < output.gtw_count; i++) {
  output["gw_" + i + "_rssi"] = input.uplink_message.rx_metadata[i].rssi;
  output["gw_" + i + "_snr"]  = input.uplink_message.rx_metadata[i].snr;
}

output.dev_id = input.end_device_ids.device_id;
output.recv_at = input.received_at;

const URL = "https://swarm.hiveeyes.org/api/" + output.dev_id.replace(/-/g, '/') + "/data";

request.body = output;
request.forwardTo = URL;
