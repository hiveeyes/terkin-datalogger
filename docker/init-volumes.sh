#!/bin/bash

VOLUMES_DIR='volumes'

mkdir -p "./${VOLUMES_DIR}/mosquitto/data"
mkdir "./${VOLUMES_DIR}/mosquitto/conf"
mkdir "./${VOLUMES_DIR}/mosquitto/log"

mkdir -p "./${VOLUMES_DIR}/influxdb/data"
mkdir "./${VOLUMES_DIR}/influxdb/conf"
mkdir "./${VOLUMES_DIR}/influxdb/log"

mkdir -p "./${VOLUMES_DIR}/grafana/data"
mkdir "./${VOLUMES_DIR}/grafana/log"

mkdir -p "./${VOLUMES_DIR}/kotori/conf/apps-enabled"
mkdir "./${VOLUMES_DIR}/kotori/log"

mkdir -p "./${VOLUMES_DIR}/mongodb/data"
mkdir "./${VOLUMES_DIR}/mongodb/log"

mkdir -p "./${VOLUMES_DIR}/redis/data"

mkdir -p "./${VOLUMES_DIR}/nginx/cert"
mkdir "./${VOLUMES_DIR}/nginx/conf.d"
