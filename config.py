""" MQTT Hiveeyes Variables """

# known wifi credentials
known_wifi_APs = [('<YOUR_WIFI_SSID_1>', '<WIFI_PASS_1>'), ('<YOUR_WIFI_SSID_2>', '<WIFI_PASS_2>')] # change this line to match your WiFi settings

# MQTT hiveeyes topic
mqtt_topic_hiveeyes = u'{realm}/{network}/{gateway}/{node}'.format(
    realm   = 'hiveeyes',
    network = 'testdrive',
    gateway = 'micropython',
    node    = 'hive_one'
)
