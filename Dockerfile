FROM tensorflow/tensorflow

RUN apt-get update && apt-get install -y redis supervisor libglu1-mesa

# application folder
RUN mkdir /app
WORKDIR /app

# python requirements
COPY ./ /app/
RUN pip install -r /app/requirements.txt

# set default environmnet variables
ENV RTSP_URL="rtsp://nutanix:test1234@192.168.101.113:8554/Streaming/Channels/101"

# Supervisor config
COPY /supervisor /src/supervisor
RUN mkdir /var/log/supervisord

# supervisord run
EXPOSE 8000
CMD ["supervisord","-c","/src/supervisor/service_script.conf"]