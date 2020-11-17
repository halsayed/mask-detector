FROM tensorflow/tensorflow

#RUN apk add --update --no-cache python3-dev libffi-dev gcc musl-dev make ffmpeg tzdata supervisor redis
#RUN rm -rf /car/cache/apk/*
#RUN apk add --update --no-cache python3-dev libffi-dev gcc tzdata supervisor redis
#RUN rm -rf /car/cache/apk/*
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

# Temp workaround to allow ssh into container
#RUN apk --update add --no-cache openssh bash \
#  && sed -i s/#PermitRootLogin.*/PermitRootLogin\ yes/ /etc/ssh/sshd_config \
#  && echo "root:root" | chpasswd \
#  && rm -rf /var/cache/apk/*
#RUN sed -ie 's/#Port 22/Port 8000/g' /etc/ssh/sshd_config
#RUN sed -ri 's/#HostKey \/etc\/ssh\/ssh_host_key/HostKey \/etc\/ssh\/ssh_host_key/g' /etc/ssh/sshd_config
#RUN sed -ir 's/#HostKey \/etc\/ssh\/ssh_host_rsa_key/HostKey \/etc\/ssh\/ssh_host_rsa_key/g' /etc/ssh/sshd_config
#RUN sed -ir 's/#HostKey \/etc\/ssh\/ssh_host_dsa_key/HostKey \/etc\/ssh\/ssh_host_dsa_key/g' /etc/ssh/sshd_config
#RUN sed -ir 's/#HostKey \/etc\/ssh\/ssh_host_ecdsa_key/HostKey \/etc\/ssh\/ssh_host_ecdsa_key/g' /etc/ssh/sshd_config
#RUN sed -ir 's/#HostKey \/etc\/ssh\/ssh_host_ed25519_key/HostKey \/etc\/ssh\/ssh_host_ed25519_key/g' /etc/ssh/sshd_config
#RUN /usr/bin/ssh-keygen -A
#RUN ssh-keygen -t rsa -b 4096 -f  /etc/ssh/ssh_host_key
#
#EXPOSE 8000
#CMD ["/usr/sbin/sshd","-D"]
# end of temp workaround
#
#
EXPOSE 8000
CMD ["supervisord","-c","/src/supervisor/service_script.conf"]