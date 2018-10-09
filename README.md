# Firmware Update Server

Serves firmware binary files for Arduino (or ESP, ...) OTA projects.

## Features
- Generic delivery of firmware images based on naming scheme
- Self contained
- SSL

## Usage
Example usage:
```
./server.py --dir=/my-firmware-directory
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

Example: Given a file with the name *firmware-0.1.bin*, this would be served with the URL:
```
http://server-ip:8000/firmware
````

