# https://github.com/pycom/pycom-libraries/tree/master/pycom-docker-fw-build

FROM python:3.9-slim-buster

RUN apt-get update && \ 
    apt-get -y install curl zip git wget && \
    apt-get -y install build-essential python3 python3-pip && \
    apt-get -y clean && \
    mkdir /opt/frozen/ && cd /opt && \
    wget -q https://dl.espressif.com/dl/xtensa-esp32-elf-linux64-1.22.0-98-g4638c4f-5.2.0-20190827.tar.gz && \
    tar -xzvf xtensa-esp32-elf-linux64-1.22.0-98-g4638c4f-5.2.0-20190827.tar.gz  && \
    git clone --recursive https://github.com/pycom/pycom-esp-idf.git    && \
    cd pycom-esp-idf && git submodule update --init && cd ..            && \
    git clone --recursive https://github.com/pycom/pycom-micropython-sigfox.git

ADD tools/pycom-firmware-build /usr/bin/build
ADD requirements-cpython.txt requirements-docs.txt requirements-build.txt requirements-dev.txt requirements-test.txt /tmp/terkin/requirements/

RUN  find /tmp/terkin/requirements/ -name "requirements*.txt" -type f -exec python3 -m pip install -r '{}' ';'

WORKDIR /src/terkin-datalogger