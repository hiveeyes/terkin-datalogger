# https://github.com/pycom/pycom-libraries/tree/master/pycom-docker-fw-build

FROM debian:buster-slim

RUN apt-get update && \ 
    apt-get install -y python3 python3-pip && \
    apt-get -y clean && \
    python3 -m pip install -U pip setuptools

# ADD requirements-cpython.txt /tmp/build/requirements.txt
# RUN python3 -m pip install -r /tmp/build/requirements.txt

ADD dist/terkin*-py3-none-any.whl /tmp/build/
RUN python3 -m pip install /tmp/build/*.whl

WORKDIR /opt/terkin-datalogger
CMD [ "terkin", "--config=settings.py", "--daemon"]