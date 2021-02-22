FROM ubuntu

LABEL maintainer="soocto@gmail.com"

ENV TZ Asia/Shanghai
ENV LANGUAGE en_US.UTF-8
ENV LC_ALL C
ENV LANG zh_CN.UTF-8
ENV DEBIAN_FRONTEND=noninteractive

RUN sed -i s@/archive.ubuntu.com/@/mirrors.aliyun.com/@g /etc/apt/sources.list
RUN apt-get clean
RUN apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends apt-utils
RUN apt-get upgrade -y
RUN apt-get install -y libxcb-xinerama0 libgl1-mesa-glx libgtk2.0-dev pkg-config curl unzip language-pack-zh-hans vim openssh-server
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py 
RUN apt-get -y install python3-setuptools
RUN python3 get-pip.py
RUN pip3 install opencv-python-headless opencv-python numpy -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com

RUN cd /root && \
wget https://github.com/loadchange/mymercury/archive/master.zip && \
unzip master.zip

RUN rm -rf /tmp/* /var/lib/apt/lists/* /var/tmp/*
RUN echo 'root:root'|chpasswd

RUN sed -ri 's/^#PermitRootLogin\s+.*/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN sed -ri 's/UsePAM yes/#UsePAM yes/g' /etc/ssh/sshd_config
RUN mkdir /var/run/sshd

EXPOSE 22

VOLUME /cctv/video

CMD ["python3", "/root/mymercury-master/run.py"]
