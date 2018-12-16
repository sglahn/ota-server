# Firmware Update Server

Serves firmware binary files for Arduino (or ESP, ...) OTA projects.

## Features
- Generic delivery of firmware images based on [Semantic Versioning](https://semver.org/spec/v2.0.0.html)
- Self contained and pure Python, no additional web server needed
- SSL

## Usage

### Testing
```
./server.py --dir=/my-firmware-directory
```

### Service
The OTA-Server can be installed as a service, which means it will be automatically started in the background after a server reboot(currently the install script is only tested on [Raspbian](https://www.raspberrypi.org/downloads/raspbian/)):
```
./install.sh
```
The logs of the service can be retrieved via:
```
sudo journalctl -u ota-server
```

### Docker
There is also a Docker image available on Docker Hub:
```
docker run -p 8000:8000 -v /my-firmware-directory:/firmware sglahn/ota-server
```

## Verify
The server can be tested with, e.g. curl:
```
url -X GET \
  http://localhost:8000/firmware \
    -H 'x-ESP8266-version: 1.0'
```    

Optional arguments:
```
  -h, --help   show this help message and exit
  --dir DIR    Directory containing the firmware binaries to serve. Default:
               ~/firmware
  --port PORT  Server port. Default: 8000.
  --log LOG    Log level. Default ERROR
  --cert CERT  SSL cert file to enable HTTPS. Default empty=No HTTPS
```

## Naming convention
The OTA-Server follows the Semantic Versioning definition. Given a version number MAJOR.MINOR.PATCH, increment the:
1. MAJOR version when you make incompatible API changes,
2. MINOR version when you add functionality in a backwards-compatible manner, and
3. PATCH version when you make backwards-compatible bug fixes.

Firmware files can be served if they follow this naming convention
```
${project-name}-${major}.${minor}.${patch}.bin
```
Valid names are *firmware-0.1.bin*, *firmware-0.1.0.bin*, invalid names are *firmware.bin*, *firmware-0.1-alpha.bin*, *firmware-0.1.zip*.

## URL Scheme
A file with the name *firmware-0.1.bin* would be served via the URL:
```
http://{host}:{port}/firmware
````
