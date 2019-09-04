# https://github.com/pycom/pycom-libraries/tree/master/pycom-docker-fw-build

FROM debian:buster-slim

RUN apt-get update && \ 
    apt-get -y install wget git build-essential python python-serial python-virtualenv python3-virtualenv && \
    mkdir /opt/frozen/ && cd /opt && \
    wget -q https://dl.espressif.com/dl/xtensa-esp32-elf-linux64-1.22.0-80-g6c4433a-5.2.0.tar.gz && \
    tar -xzvf xtensa-esp32-elf-linux64-1.22.0-80-g6c4433a-5.2.0.tar.gz  && \
    git clone --recursive https://github.com/pycom/pycom-esp-idf.git    && \
    cd pycom-esp-idf && git submodule update --init && cd ..            && \
    git clone --recursive https://github.com/pycom/pycom-micropython-sigfox.git

ADD tools/pycom-firmware-build /usr/bin/build
