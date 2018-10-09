FROM python:3.6-alpine

LABEL app.name="ota-server" \
      app.version="1.0" \
      maintainer="Sebastian Glahn <hi@sgla.hn>"

COPY server.py /opt/server.py

VOLUME ["/firmware"]

WORKDIR /opt

CMD [ "/opt/server.py", "--dir", "/firmware" ]
