#########################################
Hiveeyes MicroPython Datalogger releasing
#########################################

*****************
Cut a new release
*****************
::

    make release bump=minor


**************************************
Build and publish distribution package
**************************************
Create .tar.gz and .zip archive at ``dist`` directory, create release on GitHub and upload them::

    export GITHUB_TOKEN={redacted}
    make publish-release version=0.1.0

Create .tar.gz and .zip archive at ``dist`` directory only::

    make create-release-archives version=0.1.0
