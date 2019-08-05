download-nrf-connect:
	$(eval fetch := wget --quiet --no-clobber --show-progress --directory-prefix)
	$(fetch) bin https://github.com/NordicSemiconductor/Android-nRF-Connect/releases/download/v4.22.3/nRF.Connect.4.22.3.apk

install-nrf-connect: download-nrf-connect
	adb install bin/nRF.Connect.4.22.3.apk
