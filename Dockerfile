FROM tensorflow/tensorflow

RUN apt-get update && apt-get install -y redis supervisor libglu1-mesa

# application folder
RUN mkdir /app
WORKDIR /app

# python requirements
COPY ./model/ /app/
COPY ./static/ /app/
COPY ./supervisor/ /app/
COPY ./templates/ /app/
COPY ./requirements.txt /app/
COPY ./app.py /app/
COPY ./background_service.py /app/
COPY ./config.py /app/
COPY ./helpers.py /app/
COPY ./videoCapture.py /app/
COPY ./wsgi.py /app/
RUN pip install -r /app/requirements.txt

# set default environmnet variables
ENV RTSP_URL="rtsp://nutanix:test1234@192.168.101.113:8554/Streaming/Channels/101"

# Supervisor config
COPY /supervisor /src/supervisor
RUN mkdir /var/log/supervisord

# supervisord run
EXPOSE 8000
CMD ["supervisord","-c","/src/supervisor/service_script.conf"]