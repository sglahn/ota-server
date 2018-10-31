# Firmware Update Server

Serves firmware binary files for Arduino (or ESP, ...) OTA projects.

## Features
- Generic delivery of firmware images based on naming scheme
- Self contained, pure Python
- SSL

## Usage
Example usage:
```
./server.py --dir=/my-firmware-directory
```
Or via Docker
```
docker run -p 8000:8000 -v /my-firmware-directory:/firmware sglahn/ota-server
```

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
Firmware files can be served if they follow the naming convention
```
${project-name}-${version}.bin
```
Where both, project-name and version are Strings. 

Example: Given a file with the name *firmware-0.1.bin*, this would be served via the URL:
```
http://{host}:{port}/firmware
````
