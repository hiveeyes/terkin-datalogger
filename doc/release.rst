#########################################
Hiveeyes MicroPython Datalogger releasing
#########################################

Create .tar.gz and .zip archive at ``dist`` directory, create release on GitHub and upload them::

    export GITHUB_TOKEN={redacted}
    make publish-release version=0.1.0

Create .tar.gz and .zip archive at ``dist`` directory only::

    make create-release-archives version=0.1.0
