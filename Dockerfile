FROM ubuntu:16.04

RUN apt update
RUN DEBIAN_FRONTEND=noninteractive apt -y install python-software-properties
RUN DEBIAN_FRONTEND=noninteractive apt -y install software-properties-common
RUN DEBIAN_FRONTEND=noninteractive apt -y install git
RUN add-apt-repository ppa:jonathonf/python-3.6
RUN apt update && DEBIAN_FRONTEND=noninteractive apt -y install python3.6 python3.6-dev python3-pip
RUN apt-get clean

# Use python 3.6 by default
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.5 1
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.6 2
WORKDIR /opt
RUN git clone  http://github.com/TattiQ/kafka.git
RUN cd kafka && pip3 install --no-cache-dir -r requirements.txt
RUN chmod +x /opt/kafka/kafka_client_sf.py
CMD [ "python3.6", "-u", "/opt/kafka/kafka_client_sf.py" ]
