##############################
Docker Development Environment
##############################


*************
Prerequisites
*************
You must have the Docker CLI tools and access to a Docker Host. to check this use:::

    docker system info
    git clone https://github.com/hiveeyes/terkin-datalogger.git
    cd terkin-datalogger


**********************
Prepare working images
**********************
Use `docker compose` to build images:::

    docker compose build

Use `docker compose` to build terkin packge wheels::

    # This will generate python wheels in the `dist` folder.
    docker compose up build


*************
Configuration
*************
Create configuration from blueprint:::

    cp src/settings.raspberrypi-basic.py src/settings.py


***
Run
***
Run terkin-datalogger as a daemon within a docker compose service:::

    docker compose up daemon
    # Or in headless mode:
    docker compose up -d daemon

***********************
VSCode Remote Container
***********************
You can use the `dev` container as a basis for a VSCode remote Development Environment.
