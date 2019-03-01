
from config import *
from config_local import *

from radio import start_wifi
# Setup wifi
wifi_success = start_wifi(known_wifi_APs)
print(wifi_success)


from telemetry import TelemetryNode, TelemetryTopologies
# Create a "Node API" telemetry client object
telemetry = TelemetryNode(
    #"https://swarm.hiveeyes.org/api",
    #"http://swarm.hiveeyes.org/api-notls",
    "mqtt://swarm.hiveeyes.org",
    address = {
        "realm":    "hiveeyes",
        "network":  "testdrive",
        "gateway":  "area-23",
        "node":     "node-1",
    },
    topology = TelemetryTopologies.KotoriWanTopology
)

# Setup telemetry object
telemetry.setup()

# Transmit data
data = {"temperature": 42.84, "humidity": 83};
print(telemetry.transmit(data))
