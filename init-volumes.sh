#!/bin/bash

VOLUMES_DIR='volumes'

mkdir -p "./${VOLUMES_DIR}/mosquitto/data"
mkdir "./${VOLUMES_DIR}/mosquitto/conf"
mkdir "./${VOLUMES_DIR}/mosquitto/log"

mkdir -p "./${VOLUMES_DIR}/influxdb/data"
mkdir "./${VOLUMES_DIR}/influxdb/conf"

mkdir -p "./${VOLUMES_DIR}/grafana/data"
mkdir "./${VOLUMES_DIR}/grafana/log"

mkdir -p "./${VOLUMES_DIR}/kotori/conf/apps-enabled"
